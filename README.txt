==================================================
EA SPORTS FC LIVE TELEMETRY SYNC (v5.0 - Auto Capture + Project Atlas)
==================================================

How to send matches and transfers from the game to your phone in REAL TIME:

1. Start the Bridge on your PC:
   Double-click `Start_Bridge.bat` (or `Start_Bridge_Python.bat`).
   Keep this window open while you play!
   (Enter the displayed IP address e.g. http://192.168.x.x:5050 in your phone app under Settings -> Live Telemetry)

2. Activate the capture script in FC Live Editor (Career Mode must be loaded):
   RECOMMENDED: run `FC26_Auto_Capture.lua`.
   It watches your club in the background (every 2 seconds), then sends
     - every finished match, with real line-ups, ratings, scorers, man of the match and league position
     - every transfer (permanent and loan, in and out) as it happens
   `telemetry_auto_loop.lua` does the same: it starts FC26_Auto_Capture.lua for you.
   `telemetry_sync.lua` is the older all-in-one script; it still works and stands down by itself while
   FC26_Auto_Capture.lua is running.

   DETAILED PLAYER STATISTICS (passes, shots, tackles, xG, real ratings, man of the match) come from the
   Project Atlas exporter by its original author (r/seriousfifacareers). Keep these files together in the same
   Live Editor scripts folder:
     FC26_Auto_Capture.lua          sends everything to the phone (run this one)
     FC26_AutoCapture_v1.1.1.lua    the Atlas exporter; FC26_Auto_Capture.lua starts it for you
   When a match ends, FC26_Auto_Capture.lua waits up to 45 seconds for the exporter's files so the detailed
   numbers are included. If none arrive it sends the match from the game database instead (estimated detail).
   `FC26_MatchStatsExport.lua` and `FC26_Snapshot.lua` are the complete original exporters that are built into
   FC26_AutoCapture_v1.1.1.lua. They are only needed if you want to run the exporters on their own; do not run
   them at the same time as FC26_AutoCapture_v1.1.1.lua.

3. Playing matches (important Career Mode step):
   - When a match finishes, click 'Advance' on the post-match summary to return to the Career Central Hub.
     (EA SPORTS FC only commits results and player stats to the career database once you reach the Hub.)
   - Back on the Hub the match is sent to your phone automatically.

4. Sending things by hand (type these in the Live Editor Lua console while FC26_Auto_Capture.lua runs):
   FC26_AutoCapture_Status()            show what is waiting to be sent and the last answer from the bridge
   FC26_AutoCapture_SyncLatest()        send your latest match again
   FC26_AutoCapture_SyncTransfers()     send this season's transfers again
   FC26_BeamTransfer(name, type, fee, club)   send any transfer by hand
   `send_latest_match.lua` sends the latest match in one click.
   `telemetry_test_connection.lua` checks that the bridge is reachable and prints what is wrong if it is not.

5. If something does not arrive:
   - Delivery log: Documents\FC26 Export\bridge_send_log.txt (one line per attempt with the bridge's HTTP answer).
     200 = delivered. Anything undelivered is kept in Documents\FC26 Export\outbox and retried every
     30 seconds (also after restarting Live Editor), so nothing is lost while the bridge is closed.
   - Run `telemetry_test_connection.lua`; it reports whether the bridge answers on port 5050.
   - The bridge window prints a line for every request, every duplicate it ignored and every payload it refused.
   - Older logs: telemetry_sync_log.txt is now in Documents\FC26 Export as well.

6. Things the bridge now handles for you:
   - A match reported twice (database + Atlas export) is stored once.
   - A damaged or half-written message is refused (HTTP 400) instead of being stored, so one bad
     message can no longer stall the phone app.
   - Accented names and the euro sign arrive intact.
   - Match detail exports are found in Documents\FC26 Export even when Windows keeps Documents in OneDrive.

7. Security notes:
   - Your phone has read-only access. It only fetches /events from the bridge.
   - Anything that writes (the Live Editor Lua scripts, the dashboard test buttons, Clear) must come
     from this same PC. Writes from other devices on your network are refused (HTTP 403).
   - The Windows firewall rule created by Start_Bridge.bat only allows devices on your local subnet.
   - Web pages open in a browser cannot send data to the bridge (no CORS, Host and Origin checks).
   - The /test-match, /test-transfer and /clear links no longer work by simply opening them in a browser;
     use the buttons on the dashboard (http://localhost:5050) or Send_Test_Match.bat instead.
   - Anyone on your local network can still READ /events if they know the address. If you play on
     shared or public Wi-Fi, do not run the bridge there.

8. Test build of the Android app:
   The "fctest" build installs next to your normal app (package com.aistudio.fccareer.zqxwv.test,
   name "FC Tracker (Test)") and keeps its own data, so your real career is untouched.
   - GitHub: Actions tab -> "Build test APK" -> newest run -> Artifacts -> FC-Tracker-test-apk
   - Android Studio / command line:  gradle :app:assembleFctest
     (the APK is app/build/outputs/apk/fctest/app-fctest.apk)
