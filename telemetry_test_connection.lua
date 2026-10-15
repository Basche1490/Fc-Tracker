-- =========================================================================
-- TELEMETRY CONNECTION & BRIDGE TEST SCRIPT
-- Run this in Live Editor to verify that Live Editor can reach the Bridge!
-- =========================================================================

local function my_log(msg)
    local s = "[TelemetryTest] " .. tostring(msg)
    pcall(print, s)
end

my_log(">>> TESTING CONNECTION TO TELEMETRY BRIDGE (Port 5050) <<<")

local temp_dir = os.getenv("TEMP") or os.getenv("TMP") or "."
local temp_json = temp_dir .. "\\fifa_test_payload.json"
local temp_bat = temp_dir .. "\\fifa_test_send.bat"

local today = os.date("%Y-%m-%d")
local payload = string.format([[{
    "dataType": "match",
    "title": "Live Match Final",
    "message": "Full Time: vs 3 - 1 Arsenal (Premier League)",
    "opponentName": "Arsenal",
    "isHome": true,
    "goalsFor": 3,
    "goalsAgainst": 1,
    "resultBadge": "W",
    "date": "%s",
    "competition": "Premier League",
    "stage": "Matchday 10",
    "shotsFor": 14,
    "shotsAgainst": 5,
    "possession": 58,
    "passingAccuracy": 89,
    "expectedGoals": 2.65,
    "expectedGoalsAgainst": 0.85,
    "leaguePosition": 1,
    "motmName": "Bukayo Saka",
    "playerPerformances": [
        {"playerName": "Bukayo Saka", "goals": 2, "assists": 1, "rating": 9.2, "passes": 42, "passAccuracy": 88, "shots": 4, "shotAccuracy": 75, "saves": 0, "penaltySaves": 0, "tackles": 1, "tacklePercentage": 100, "interceptions": 0, "cleanSheet": false, "yellowCard": false, "redCard": false, "isMotm": true},
        {"playerName": "Declan Rice", "goals": 1, "assists": 0, "rating": 8.1, "passes": 68, "passAccuracy": 92, "shots": 2, "shotAccuracy": 50, "saves": 0, "penaltySaves": 0, "tackles": 5, "tacklePercentage": 80, "interceptions": 3, "cleanSheet": false, "yellowCard": true, "redCard": false, "isMotm": false},
        {"playerName": "Martin Odegaard", "goals": 0, "assists": 2, "rating": 8.5, "passes": 55, "passAccuracy": 91, "shots": 1, "shotAccuracy": 100, "saves": 0, "penaltySaves": 0, "tackles": 2, "tacklePercentage": 50, "interceptions": 1, "cleanSheet": false, "yellowCard": false, "redCard": false, "isMotm": false}
    ],
    "goalDetails": [
        {"playerName": "Bukayo Saka", "minute": 24, "isOpponent": false},
        {"playerName": "Declan Rice", "minute": 58, "isOpponent": false},
        {"playerName": "Bukayo Saka", "minute": 76, "isOpponent": false},
        {"playerName": "Gabriel Martinelli (Opponent)", "minute": 83, "isOpponent": true}
    ]
}]], today)

local f = io.open(temp_json, "wb")
if f then
    f:write(payload)
    f:close()
    my_log("Wrote test payload (" .. tostring(#payload) .. " bytes)")
end

local bf = io.open(temp_bat, "w")
if bf then
    bf:write(string.format([[@echo off
curl -s -X POST -H "Content-Type: application/json; charset=utf-8" --data-binary @"%s" http://127.0.0.1:5050
if %%ERRORLEVEL%% NEQ 0 (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-RestMethod -Uri 'http://127.0.0.1:5050' -Method POST -ContentType 'application/json; charset=utf-8' -InFile '%s'; Write-Host 'Dispatched via PowerShell' } catch { Write-Host 'Failed to connect to bridge: ' $_.Exception.Message }"
)
]], temp_json, temp_json))
    bf:close()
    my_log("Dispatching to Bridge http://127.0.0.1:5050...")
    os.execute(string.format('start /B "" "%s"', temp_bat))
    my_log(">>> TEST SENT! Look at your bridge command prompt and Android App!")
end
