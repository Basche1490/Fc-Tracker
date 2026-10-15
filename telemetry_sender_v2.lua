-- =========================================================================
-- FIFA LIVE EDITOR TELEMETRY SENDER V2
-- Sends structured JSON data to Python Bridge for mapping to Android AppState
-- =========================================================================

local function escape_str(s)
    if s == nil then return "" end
    s = tostring(s)
    s = s:gsub('\\', '\\\\'):gsub('"', '\\"'):gsub('\n', '\\n'):gsub('\r', '')
    return s
end

local function send_to_bridge(json_payload)
    local url = "http://localhost:8080"
    -- Safely wrap the payload for curl execution in Windows cmd
    local safe_payload = json_payload:gsub('"', '\\"')
    local cmd = string.format('curl -s -X POST -H "Content-Type: application/json" -d "%s" %s', safe_payload, url)
    os.execute(cmd)
end

-- 1. SEND TRANSFER EVENT
function send_transfer_event(player_name, transfer_type, fee_millions, from_to_club, date_str)
    local msg = string.format("%s %s for £%.1fM", player_name, transfer_type, fee_millions)
    local payload = string.format([[
    {
        "dataType": "transfer",
        "title": "Transfer Activity",
        "message": "%s",
        "playerName": "%s",
        "type": "%s",
        "feeM": %.2f,
        "fromToClub": "%s",
        "date": "%s"
    }]], escape_str(msg), escape_str(player_name), escape_str(transfer_type), fee_millions, escape_str(from_to_club), escape_str(date_str))
    
    send_to_bridge(payload)
end

-- 2. SEND MATCH RESULT
function send_match_result(opponent_name, is_home, goals_for, goals_against, date_str, competition)
    local badge = "D"
    if goals_for > goals_against then badge = "W"
    elseif goals_against > goals_for then badge = "L" end
    
    local loc = is_home and "vs" or "@"
    local msg = string.format("Full Time: %s %d - %d %s", loc, goals_for, goals_against, opponent_name)
    
    local payload = string.format([[
    {
        "dataType": "match",
        "title": "Match Result",
        "message": "%s",
        "opponentName": "%s",
        "isHome": %s,
        "goalsFor": %d,
        "goalsAgainst": %d,
        "resultBadge": "%s",
        "date": "%s",
        "competition": "%s"
    }]], escape_str(msg), escape_str(opponent_name), is_home and "true" or "false", goals_for, goals_against, badge, escape_str(date_str), escape_str(competition))
    
    send_to_bridge(payload)
end

-- 3. SEND INJURY REPORT
function send_injury_report(player_name, injury_type, duration_days)
    local msg = string.format("%s suffered a %s (Out for ~%d days)", player_name, injury_type, duration_days)
    local payload = string.format([[
    {
        "dataType": "injury",
        "title": "Medical Report",
        "message": "%s",
        "playerName": "%s",
        "duration": %d
    }]], escape_str(msg), escape_str(player_name), duration_days)
    
    send_to_bridge(payload)
end

-- =========================================================================
-- EXAMPLE TRIGGERS:
-- (Uncomment and run these inside Live Editor to test the bridge!)
-- =========================================================================
-- send_transfer_event("B. Hettwer", "Transfer In", 3.5, "From MSV Duisburg", "2025-08-14")
-- send_match_result("Wrexham", true, 2, 0, "2025-08-16", "EFL League Two")
-- send_injury_report("L. Jephcott", "Sprained Ankle", 21)
