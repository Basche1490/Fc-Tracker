import http.server
import socketserver
import json
import time
import os
import socket
import re
import html
import ipaddress
from urllib.parse import urlsplit

LOCAL_PORT = 5050
EVENTS_FILE = os.path.join(os.path.dirname(__file__), "telemetry_events.json")
MAX_BODY_BYTES = 5 * 1024 * 1024  # largest POST body the bridge will accept (5 MiB)

# ---------------------------------------------------------------------------
# Access control
#
# The phone only ever READS (GET /events). Everything that writes - the Lua
# scripts, the test buttons and /clear - runs on this same PC. So reads are open
# to the local network, but writes are only accepted from the PC itself.
# Host / Origin checks keep web pages open in a browser from reaching the bridge.
# ---------------------------------------------------------------------------
PC_NAME = socket.gethostname().lower()


def _strip_mapped(addr):
    addr = (addr or "").strip()
    if addr.lower().startswith("::ffff:"):
        return addr[7:]
    return addr


def is_local_client(client_ip, server_ip):
    """True when the request comes from this PC (loopback, or the PC's own LAN address)."""
    client_ip = _strip_mapped(client_ip)
    server_ip = _strip_mapped(server_ip)
    try:
        if ipaddress.ip_address(client_ip).is_loopback:
            return True
    except ValueError:
        return False
    return client_ip == server_ip


def _host_only(host_header):
    h = (host_header or "").strip()
    if h.startswith("["):                  # [::1]:5050
        end = h.find("]")
        return h[1:end] if end != -1 else h
    if h.count(":") == 1:                  # name:port or 1.2.3.4:port
        return h.split(":")[0]
    return h


def host_header_ok(host_header):
    """Allow IP addresses, localhost and this PC's name. Other hostnames are refused
    so a malicious web page cannot reach the bridge through DNS rebinding."""
    host = _host_only(host_header).lower()
    if not host:
        return True                        # HTTP/1.0 client without a Host header - not a browser
    if host in ("localhost", PC_NAME, PC_NAME + ".local"):
        return True
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def origin_ok(origin, host_header, sec_fetch_site=None):
    """Writes may come from command-line tools (no Origin header) or from this
    bridge's own dashboard page. A page on any other site is refused."""
    if not origin:
        return (sec_fetch_site or "none").lower() in ("none", "same-origin")
    try:
        netloc = urlsplit(origin).netloc.lower()
    except ValueError:
        return False
    return bool(netloc) and netloc == (host_header or "").strip().lower()

def sanitize_penalty_text(text):
    if not text:
        return text
    s = str(text)
    s = re.sub(r'\s*\(Pens:\s*255-\d+\)', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*\(Pens:\s*\d+-255\)', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s*\(Pens:\s*0-0\)', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\b255\s*penalties\b', '0 penalties', s, flags=re.IGNORECASE)
    return s

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# Load or init events
events = []
if os.path.exists(EVENTS_FILE):
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8") as f:
            raw_evs = json.load(f)
            for ev in raw_evs:
                if isinstance(ev, dict):
                    if "message" in ev and isinstance(ev["message"], str):
                        ev["message"] = sanitize_penalty_text(ev["message"])
                    events.append(ev)
    except Exception:
        events = []

def save_events():
    try:
        with open(EVENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(events, f)
    except Exception:
        pass

def add_event(title, msg, raw_payload=None):
    ts = int(time.time())
    ev = {
        "event": "message",
        "id": f"ev-{ts}-{len(events)}",
        "time": ts,
        "title": title,
        "message": raw_payload if raw_payload else msg
    }
    events.append(ev)
    if len(events) > 100:
        events.pop(0)
    save_events()
    print(f"[{time.strftime('%H:%M:%S')}] TELEMETRY SAVED: {title}")

def create_sample_match():
    today = time.strftime("%Y-%m-%d")
    return {
        "dataType": "match",
        "title": "Live Match Final",
        "message": "Full Time: vs 3 - 1 Arsenal (Premier League)",
        "opponentName": "Arsenal",
        "isHome": True,
        "goalsFor": 3,
        "goalsAgainst": 1,
        "resultBadge": "W",
        "date": today,
        "competition": "Premier League",
        "shotsFor": 12,
        "shotsAgainst": 6,
        "possession": 56,
        "passingAccuracy": 88,
        "expectedGoals": 2.8,
        "expectedGoalsAgainst": 0.9,
        "playerPerformances": [
            {"playerName": "Bukayo Saka", "goals": 2, "assists": 1, "rating": 8.9, "yellowCard": False, "redCard": False},
            {"playerName": "Declan Rice", "goals": 1, "assists": 0, "rating": 7.8, "yellowCard": True, "redCard": False},
            {"playerName": "Martin Odegaard", "goals": 0, "assists": 2, "rating": 8.4, "yellowCard": False, "redCard": False}
        ],
        "goalDetails": [
            {"playerName": "Bukayo Saka", "isOpponent": False},
            {"playerName": "Declan Rice", "isOpponent": False},
            {"playerName": "Bukayo Saka", "isOpponent": False},
            {"playerName": "Kai Havertz (Opponent)", "isOpponent": True}
        ]
    }

class TelemetryHandler(http.server.BaseHTTPRequestHandler):
    timeout = 15  # drop clients that stall in the middle of a request

    def end_headers(self):
        # Deliberately no CORS headers: the phone app is not a browser and the
        # dashboard page is served from this same origin.
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def _reject(self, code, message):
        body = json.dumps({"status": "error", "message": message}).encode()
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _host_allowed(self):
        if host_header_ok(self.headers.get('Host')):
            return True
        self._reject(403, "Unexpected Host header.")
        return False

    def _write_allowed(self):
        """Gate for anything that changes state. Sends the error reply itself when refusing."""
        if not self._host_allowed():
            return False
        server_ip = self.connection.getsockname()[0]
        if not is_local_client(self.client_address[0], server_ip):
            self._reject(403, "Writes are only accepted from the PC running the bridge.")
            return False
        if not origin_ok(self.headers.get('Origin'), self.headers.get('Host'), self.headers.get('Sec-Fetch-Site')):
            self._reject(403, "Cross-site request blocked.")
            return False
        return True

    def do_OPTIONS(self):
        # No CORS preflight support - browsers on other sites must not be able to write.
        self._reject(405, "Method not allowed.")

    def do_POST(self):
        if not self._write_allowed():
            return
        path = self.path.lower()
        if path == "/test-match":
            sample = create_sample_match()
            add_event("Live Match Final", "Full Time: vs 3 - 1 Arsenal (Premier League)", json.dumps(sample))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok","message":"Test match sent successfully!"}')
            return

        if path == "/test-transfer":
            sample = {
                "dataType": "transfer",
                "title": "Transfer Finalized",
                "message": "Erling Haaland signed from Manchester City for €120.0M",
                "playerName": "Erling Haaland",
                "type": "Bought",
                "feeM": 120.0,
                "fromToClub": "Manchester City",
                "date": time.strftime("%Y-%m-%d")
            }
            add_event("Transfer Finalized", sample["message"], json.dumps(sample))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok","message":"Test transfer sent successfully!"}')
            return

        if path == "/clear":
            events.clear()
            save_events()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"cleared"}')
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
        except ValueError:
            self._reject(400, "Bad Content-Length.")
            return
        if content_length < 0:
            self._reject(400, "Bad Content-Length.")
            return
        if content_length > MAX_BODY_BYTES:
            self._reject(413, "Payload too large.")
            return
        post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
        
        try:
            data = json.loads(post_data)
            title = data.get("title", "Match Update")
            msg = sanitize_penalty_text(data.get("message", post_data))
            add_event(title, msg, post_data)
        except Exception:
            if post_data.strip():
                clean_raw = sanitize_penalty_text(post_data)
                add_event("Match Update", clean_raw, post_data)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def do_GET(self):
        if not self._host_allowed():
            return
        path = self.path.lower()
        if path in ("/test-match", "/test-transfer", "/clear"):
            # These used to fire on a plain GET, which means a link or <img> tag on any
            # web page could trigger them. They are POST-only now (use the dashboard buttons).
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return

        if path in ["/events", "/json", "/api/telemetry"]:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(events).encode())
            return

        local_ip = get_local_ip()
        page = f"""<!DOCTYPE html>
<html>
<head>
    <title>EA FC Telemetry Bridge (Python)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 24px; margin: 0; }}
        .card {{ background: #1e293b; border-radius: 14px; padding: 24px; max-width: 680px; margin: 0 auto; }}
        h1 {{ color: #38bdf8; font-size: 22px; }}
        .info {{ background: #0f172a; padding: 14px; border-radius: 8px; font-family: monospace; margin: 14px 0; border: 1px solid #334155; }}
        button, a.btn {{ background: #10b981; color: white; border: none; padding: 10px 16px; border-radius: 8px; cursor: pointer; font-weight: bold; text-decoration: none; display: inline-block; margin-right: 8px; }}
        button.blue {{ background: #0284c7; }}
        button.red {{ background: #ef4444; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>⚽ EA Sports FC Telemetry Bridge (Python)</h1>
        <div class="info">
            <strong>📱 IP Address for Android App:</strong><br>
            <span style="color:#10b981;font-size:16px;font-weight:bold;">http://{local_ip}:{LOCAL_PORT}</span>
        </div>
        <div style="margin: 16px 0;">
            <button onclick="fetch('/test-match', {{method:'POST'}}).then(()=>location.reload())">⚡ Send Test Match (3 - 1 vs Arsenal)</button>
            <button class="blue" onclick="fetch('/test-transfer', {{method:'POST'}}).then(()=>location.reload())">⚡ Send Test Transfer (€120M)</button>
            <button class="red" onclick="fetch('/clear', {{method:'POST'}}).then(()=>location.reload())">🗑️ Clear</button>
        </div>
        <p style="font-size:12px;color:#94a3b8;"><a href="/events" target="_blank" style="color:#38bdf8;">[View JSON]</a></p>
        <h3>Live Events ({len(events)} queued)</h3>
        <pre style="background:#0f172a;padding:12px;border-radius:8px;max-height:260px;overflow:auto;font-size:12px;color:#cbd5e1;">{html.escape(json.dumps(events, indent=2))}</pre>
    </div>
</body>
</html>"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))

    def log_message(self, format, *args):
        pass


import threading
import csv

processed_atlas_folders = set()

def watch_atlas_exports():
    while True:
        try:
            docs = os.path.join(os.path.expanduser("~"), "Documents", "FC26 Export")
            if os.path.exists(docs):
                match_stats_ready = os.path.join(docs, "MatchStats", "ready")
                snapshots_ready = os.path.join(docs, "Snapshots", "ready")

                if os.path.exists(match_stats_ready):
                    folders = [os.path.join(match_stats_ready, d) for d in os.listdir(match_stats_ready) if os.path.isdir(os.path.join(match_stats_ready, d))]
                    folders.sort(key=os.path.getmtime, reverse=True)

                    for folder in folders:
                        folder_id = os.path.basename(folder)
                        if folder_id in processed_atlas_folders:
                            continue

                        ready_file = os.path.join(folder, "MATCH_READY")
                        alt_ready = os.path.join(folder, "READY_FOR_MANUAL_ZIP_AND_UPLOAD.txt")
                        part_csv = os.path.join(folder, "16_match_participants_wide.csv")
                        teams_csv = os.path.join(folder, "18_match_teams_wide.csv")

                        if (os.path.exists(ready_file) or os.path.exists(alt_ready)) and os.path.exists(part_csv) and os.path.exists(teams_csv):
                            print(f"\n[PROJECT ATLAS] 🎯 New MatchStats export detected: {folder_id}")

                            opp_name = "Opponent"
                            managed_club_name = "My Club"
                            managed_team_id = 0
                            current_league_name = "League"
                            comp_name = "League Match"
                            is_home = True
                            managed_score = 0
                            opponent_score = 0
                            result_badge = "W"
                            match_date = time.strftime("%Y-%m-%d")
                            league_pos = None
                            completed_matches = []
                            managed_squad_player_ids = set()

                            if os.path.exists(snapshots_ready):
                                s_folders = [os.path.join(snapshots_ready, d) for d in os.listdir(snapshots_ready) if os.path.isdir(os.path.join(snapshots_ready, d))]
                                s_folders.sort(key=os.path.getmtime, reverse=True)
                                if s_folders:
                                    latest_snap = s_folders[0]
                                    s_matches_csv = os.path.join(latest_snap, "managed_team_matches.csv")
                                    s_leagues_csv = os.path.join(latest_snap, "team_leagues.csv")
                                    s_meta_csv = os.path.join(latest_snap, "career_metadata.csv")
                                    s_rosters_csv = os.path.join(latest_snap, "rosters.csv")

                                    if os.path.exists(s_meta_csv):
                                        with open(s_meta_csv, "r", encoding="utf-8-sig") as mf:
                                            for row in csv.DictReader(mf):
                                                if row.get("key") == "managed_team_id" and row.get("value"):
                                                    try: managed_team_id = int(row["value"])
                                                    except: pass
                                                if row.get("key") == "managed_team_name" and row.get("value"):
                                                    managed_club_name = row["value"]

                                    if os.path.exists(s_matches_csv):
                                        with open(s_matches_csv, "r", encoding="utf-8-sig") as mf:
                                            m_rows = list(csv.DictReader(mf))
                                            completed_matches = [r for r in m_rows if str(r.get("is_completed", "")).strip() in ("1", 1)]
                                            if completed_matches:
                                                latest = completed_matches[-1]
                                                managed_club_name = latest.get("managed_team_name") or managed_club_name
                                                opp_name = latest.get("opponent_team_name") or opp_name
                                                is_home = (latest.get("side", "").upper() == "HOME" or latest.get("managed_team_side", "").upper() == "HOME")
                                                managed_score = int(latest.get("managed_score", 0) or 0)
                                                opponent_score = int(latest.get("opponent_score", 0) or 0)
                                                result_badge = latest.get("result") or latest.get("managed_team_result") or ("W" if managed_score > opponent_score else ("D" if managed_score == opponent_score else "L"))
                                                match_date = latest.get("date") or match_date
                                                if latest.get("managed_team_id"):
                                                    try: managed_team_id = int(latest["managed_team_id"])
                                                    except: pass

                                    # Pick Primary League by max matches_played in team_leagues.csv
                                    if os.path.exists(s_leagues_csv):
                                        with open(s_leagues_csv, "r", encoding="utf-8-sig") as lf:
                                            best_pld = -1
                                            for tl in csv.DictReader(lf):
                                                tid = int(tl.get("team_id") or 0)
                                                tname = tl.get("team_name") or ""
                                                if tid == managed_team_id or (managed_club_name and managed_club_name.lower() in tname.lower()):
                                                    pld = int(tl.get("matches_played") or 0)
                                                    pos_val = int(tl.get("current_table_position") or 0)
                                                    if pld > best_pld and pos_val > 0:
                                                        best_pld = pld
                                                        league_pos = pos_val
                                                        if tl.get("league_name"): current_league_name = tl["league_name"]
                                                    elif best_pld == -1 and pos_val > 0:
                                                        league_pos = pos_val
                                                        if tl.get("league_name"): current_league_name = tl["league_name"]

                                    # Extract Managed Squad player IDs
                                    if os.path.exists(s_rosters_csv):
                                        with open(s_rosters_csv, "r", encoding="utf-8-sig") as rf:
                                            for r in csv.DictReader(rf):
                                                rtid = int(r.get("team_id") or 0)
                                                if rtid == managed_team_id and r.get("player_id"):
                                                    try: managed_squad_player_ids.add(int(r["player_id"]))
                                                    except: pass

                            # Determine Playoff vs Regular League vs Cup
                            raw_comp = latest.get("competition_name") if "latest" in locals() and latest.get("competition_name") else current_league_name
                            is_playoff = any(k in raw_comp.lower() for k in ["play-off", "playoff", "promotion"])
                            is_regular_league = (not is_playoff) and any(k in raw_comp.lower() for k in [current_league_name.lower(), "league", "championship", "division", "premier"]) and not any(k in raw_comp.lower() for k in ["cup", "fa", "carabao", "trophy"])

                            if is_playoff:
                                comp_name = current_league_name
                                playoff_matches = [m for m in completed_matches if any(k in (m.get("competition_name") or "").lower() for k in ["play-off", "playoff", "promotion"])]
                                p_count = max(1, len(playoff_matches))
                                if p_count >= 3: stage_val = "Play-off Final"
                                elif p_count == 2: stage_val = "Play-off Semi-Final (Leg 2)"
                                else: stage_val = "Play-off Semi-Final (Leg 1)"
                            elif is_regular_league:
                                comp_name = current_league_name
                                league_matches = [m for m in completed_matches if any(k in (m.get("competition_name") or "").lower() for k in [current_league_name.lower(), "league", "championship", "division", "premier"]) and not any(k in (m.get("competition_name") or "").lower() for k in ["play-off", "playoff", "cup", "fa", "carabao", "trophy"])]
                                stage_val = f"Matchday {max(1, len(league_matches))}"
                            else:
                                comp_name = raw_comp
                                cup_matches = [m for m in completed_matches if m.get("competition_name") == raw_comp]
                                c_count = max(1, len(cup_matches))
                                if "fa cup" in raw_comp.lower() or "emirates" in raw_comp.lower():
                                    if c_count >= 6: stage_val = "Final"
                                    elif c_count == 5: stage_val = "Semi-Final"
                                    elif c_count == 4: stage_val = "Quarter-Final"
                                    elif c_count == 3: stage_val = "Round 5"
                                    elif c_count == 2: stage_val = "Round 4"
                                    else: stage_val = "Round 3"
                                elif "carabao" in raw_comp.lower() or "efl cup" in raw_comp.lower():
                                    if c_count >= 6: stage_val = "Final"
                                    elif c_count == 5: stage_val = "Semi-Final"
                                    elif c_count == 4: stage_val = "Quarter-Final"
                                    else: stage_val = f"Round {c_count}"
                                else:
                                    stage_val = f"Round {c_count}"

                            # Parse participants
                            participants = []
                            with open(part_csv, "r", encoding="utf-8-sig") as pf:
                                participants = list(csv.DictReader(pf))

                            count0 = 0
                            count1 = 0
                            max_minutes = 0
                            for p in participants:
                                pid = int(p.get("player_id") or 0)
                                p_team = int(p.get("team_index") or 0)
                                mins = int(p.get("minutes_played") or 0)
                                if mins > max_minutes: max_minutes = mins
                                if pid in managed_squad_player_ids:
                                    if p_team == 0: count0 += 1
                                    else: count1 += 1

                            if count0 > count1:
                                managed_team_idx = 0
                                opp_team_idx = 1
                            elif count1 > count0:
                                managed_team_idx = 1
                                opp_team_idx = 0
                            else:
                                managed_team_idx = 0 if is_home else 1
                                opp_team_idx = 1 if managed_team_idx == 0 else 0

                            # Parse team stats from 18_match_teams_wide.csv
                            team_rows = []
                            with open(teams_csv, "r", encoding="utf-8-sig") as tf:
                                team_rows = list(csv.DictReader(tf))

                            m_team = team_rows[managed_team_idx] if len(team_rows) > managed_team_idx else (team_rows[0] if team_rows else {})
                            o_team = team_rows[opp_team_idx] if len(team_rows) > opp_team_idx else (team_rows[1] if len(team_rows) > 1 else {})

                            # Real Extra Time & Penalties extraction
                            is_playoff_leg1 = is_playoff and ("leg 1" in stage_val.lower())
                            if is_regular_league or is_playoff_leg1:
                                is_extra_time = False
                                home_pen = 0
                                away_pen = 0
                            else:
                                m_shootout = int(m_team.get("shootout_goals") or 0)
                                o_shootout = int(o_team.get("shootout_goals") or 0)
                                if m_shootout >= 255 or m_shootout < 0: m_shootout = 0
                                if o_shootout >= 255 or o_shootout < 0: o_shootout = 0
                                is_extra_time = (max_minutes >= 115) or (m_shootout > 0 or o_shootout > 0)
                                home_pen = m_shootout if is_home else o_shootout
                                away_pen = o_shootout if is_home else m_shootout

                            if home_pen >= 255 or home_pen < 0: home_pen = 0
                            if away_pen >= 255 or away_pen < 0: away_pen = 0

                            # Man of the Match directly from the game's man_of_the_match column
                            top_player = ""
                            highest_rating = -1.0
                            for p in participants:
                                r = float(p.get("game_rating") or 6.0)
                                is_motm = (p.get("man_of_the_match", "").lower() in ("true", "1"))
                                if is_motm and p.get("player_name"):
                                    top_player = p.get("player_name", "")
                                    break
                                if r > highest_rating and p.get("player_name"):
                                    highest_rating = r
                                    top_player = p.get("player_name", "")

                            shots_for = int(m_team.get("shots", max(managed_score + 4, 10)) or 10)
                            shots_against = int(o_team.get("shots", max(opponent_score + 2, 5)) or 5)
                            xg_f = float(m_team.get("npk_expected_goals", managed_score * 0.85 + 0.3) or 1.5)
                            xg_a = float(o_team.get("npk_expected_goals", opponent_score * 0.75 + 0.2) or 0.8)
                            passes_f = int(m_team.get("passes", 400) or 400)
                            passes_a = int(o_team.get("passes", 360) or 360)
                            pass_acc = int(float(m_team.get("pass_accuracy_pct_derived", 86) or 86))
                            poss = int(float(m_team.get("possession") or m_team.get("possession_pct") or 0))
                            if poss <= 0 and (passes_f + passes_a) > 0:
                                poss = int((passes_f / (passes_f + passes_a)) * 100)
                            if poss <= 0: poss = 52

                            # Parse real player performances from 16_match_participants_wide.csv
                            player_perfs = []
                            goal_details = []

                            for p in participants:
                                p_team = int(p.get("team_index", 0) or 0)
                                if p_team == managed_team_idx:
                                    p_name = p.get("player_name", "Player")
                                    p_id = p.get("player_id", "")
                                    p_goals = int(p.get("goals_derived") or p.get("npk_goals") or 0)
                                    p_assists = int(p.get("assists") or 0)
                                    p_rating = float(p.get("game_rating") or 7.0)
                                    p_passes = int(p.get("passes") or 30)
                                    p_pacc = int(float(p.get("pass_accuracy_pct_derived") or 82))
                                    p_shots = int(p.get("shots") or p_goals)
                                    p_sacc = int((int(p.get("shots_on_target", 0) or 0) / max(1, p_shots)) * 100) if p_shots > 0 else 0
                                    p_tackles = int(p.get("tackles") or 2)
                                    p_tpct = int(float(p.get("stand_tackle_success_pct_derived") or 80)) if p.get("stand_tackle_success_pct_derived") else 80
                                    is_motm = (p_name == top_player or p.get("man_of_the_match", "").lower() in ("true", "1"))

                                    player_perfs.append({
                                        "playerId": str(p_id),
                                        "playerName": p_name,
                                        "rating": round(p_rating, 1),
                                        "goals": p_goals,
                                        "assists": p_assists,
                                        "passes": p_passes,
                                        "passAccuracy": p_pacc,
                                        "shots": p_shots,
                                        "shotAccuracy": p_sacc,
                                        "tackles": p_tackles,
                                        "tacklePercentage": p_tpct,
                                        "interceptions": int(p.get("interceptions") or 0),
                                        "cleanSheet": (opponent_score == 0),
                                        "yellowCard": int(p.get("yellow_card_events") or 0) > 0,
                                        "redCard": int(p.get("red_dismissals") or 0) > 0,
                                        "isMotm": is_motm
                                    })

                                    for g in range(p_goals):
                                        goal_details.append({
                                            "playerName": p_name,
                                            "minute": 15 + ((g + 1) * 24),
                                            "isOpponent": False
                                        })

                            if opponent_score > 0:
                                for og in range(opponent_score):
                                    goal_details.append({
                                        "playerName": f"{opp_name} Goal",
                                        "minute": 20 + ((og + 1) * 22),
                                        "isOpponent": True
                                    })

                            loc_symbol = "vs" if is_home else "@"
                            et_str = f" (Pens: {home_pen}-{away_pen})" if (home_pen > 0 or away_pen > 0) else (" (A.E.T.)" if is_extra_time else "")
                            msg = f"Full Time: {managed_club_name} {loc_symbol} {managed_score} - {opponent_score} {opp_name} ({comp_name} - {stage_val}){et_str}"
                            match_payload = {
                                "dataType": "match",
                                "title": "Live Match Final",
                                "message": msg,
                                "opponentName": opp_name,
                                "isHome": is_home,
                                "goalsFor": managed_score,
                                "goalsAgainst": opponent_score,
                                "resultBadge": result_badge,
                                "date": match_date,
                                "competition": comp_name,
                                "stage": stage_val,
                                "isExtraTime": is_extra_time,
                                "homePenalties": home_pen,
                                "awayPenalties": away_pen,
                                "shotsFor": shots_for,
                                "shotsAgainst": shots_against,
                                "possession": poss,
                                "passingAccuracy": pass_acc,
                                "expectedGoals": round(xg_f, 2),
                                "expectedGoalsAgainst": round(xg_a, 2),
                                "motmName": top_player,
                                "leaguePosition": league_pos if (league_pos and league_pos > 0) else None,
                                "playerPerformances": player_perfs,
                                "goalDetails": goal_details
                            }

                            add_event("Live Match Final", msg, json.dumps(match_payload))
                            print(f"  -> ⚽ Imported Match: {msg}")
                            print(f"     xG: {round(xg_f, 2)} - {round(xg_a, 2)} | MOTM: {top_player} | Lineup: {len(player_perfs)} players")
                            processed_atlas_folders.add(folder_id)
        except Exception as e:
            pass
        time.sleep(2)

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = LOCAL_PORT
    print("===================================================")
    print(f" EA SPORTS FC TELEMETRY BRIDGE (Python)")
    print(f" ⭐ ENTER IN YOUR ANDROID APP:")
    print(f"    http://{local_ip}:{port}")
    print(f" Web Dashboard: http://localhost:{port}")
    print(" Phone access is read-only; writes are accepted from this PC only.")
    print(" Keep this window open while playing!")
    print("===================================================")

    class ReusableServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True
        
    try:
        threading.Thread(target=watch_atlas_exports, daemon=True).start()
        print("🟢 Project Atlas hot-folder auto-importer active (Documents\\FC26 Export)")
        with ReusableServer(("", port), TelemetryHandler) as httpd:
            print(f"🟢 Python Bridge actively listening on Port {port}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down bridge...")
    except Exception as e:
        print(f"⚠️ Port {port} listener error: {e}")
