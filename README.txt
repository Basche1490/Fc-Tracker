==================================================
EA SPORTS FC / FIFA LIVE TELEMETRY SYNC (v4.6 - Universal Match & Career Tracker)
==================================================

How to sync matches and transfers automatically from the game to your phone in REAL TIME:

1. Start the Bridge on your PC:
   Double-click `Start_Bridge.bat` (or `Start_Bridge_Python.bat`).
   Keep this window open while you play!
   (Enter the displayed IP address e.g. http://192.168.x.x:5050 in your phone app under Settings -> Live Telemetry)

2. Activate Sync in Live Editor:
   In FIFA / EA FC Live Editor, open and run `telemetry_sync.lua`.
   It automatically detects your club (e.g. Torquay United), active league, squad, and past matches.
   If Live Editor supports timers, it will poll continuously in the background every 3 seconds.
   If timers are not supported, you can assign hotkey F9 to `telemetry_sync.lua`.

3. Playing Matches (Important Career Mode Step):
   - In Career Mode, when a match finishes:
     Click 'Advance' on the post-match summary screen to return to the Career Central Hub.
     (EA Sports FC only commits your match results, standings, and player stats to the career database once you return to the Central Hub!)
   - Once back on the Central Hub, the script automatically detects the match and beams it to your phone!
   - You can also tap F9 anytime to trigger an immediate check.

4. One-Click Instant Sync:
   - If you ever want to immediately send your latest match without waiting for deltas, simply run `send_latest_match.lua` in Live Editor!
   - It grabs your club's latest match, real player stats, ratings, and goals, and beams it directly to the bridge in 0.05 seconds!

5. Diagnostic Logs:
   - Check `telemetry_sync_log.txt` on your Desktop to see detailed status and match deltas.
