-- =========================================================================
-- EA SPORTS FC TELEMETRY AUTO-LOOP LAUNCHER (OPTION B - FULLY AUTOMATIC)
-- Starts continuous background telemetry polling in Live Editor.
-- Zero hotkeys or manual clicks needed while playing!
-- =========================================================================

local function my_log(msg)
    local s = "[TelemetryAutoLoop] " .. tostring(msg)
    pcall(print, s)
end

my_log("==========================================================")
my_log("EA FC LIVE TELEMETRY: OPTION B (FULLY AUTOMATIC)")
my_log("==========================================================")

-- Helper function to find telemetry_sync.lua across all folders
local function get_sync_script_path()
    local userProfile = os.getenv("USERPROFILE") or ""
    local candidatePaths = {
        userProfile .. "\\Desktop\\FC26-LE\\FC 26 LE v26.3.6\\lua\\scripts\\telemetry_sync.lua",
        userProfile .. "\\Desktop\\FC26-LE\\telemetry_sync.lua",
        "telemetry_sync.lua",
        "FC 26 LE v26.3.6\\lua\\scripts\\telemetry_sync.lua",
        "lua\\scripts\\telemetry_sync.lua",
        userProfile .. "\\Desktop\\telemetry_sync.lua",
        userProfile .. "\\Downloads\\telemetry_sync.lua"
    }
    for _, p in ipairs(candidatePaths) do
        local f = io.open(p, "r")
        if f then
            f:close()
            return p
        end
    end
    return "telemetry_sync.lua"
end

local syncPath = get_sync_script_path()
my_log("Loading telemetry script: " .. syncPath)

local ok, err = pcall(dofile, syncPath)
if not ok then
    my_log("Error starting automatic telemetry sync: " .. tostring(err))
    print("[TelemetryAutoLoop ERROR] " .. tostring(err))
else
    my_log("🟢 OPTION B IS RUNNING IN BACKGROUND!")
    print("==========================================================")
    print(" [OPTION B ACTIVE] FULLY AUTOMATIC MODE ENGAGED")
    print(" 1. Career Mode updates will be detected automatically.")
    print(" 2. Played matches will beam to your phone on Full Time.")
    print(" 3. Transfers and signings will beam when completed.")
    print(" No hotkeys or manual button clicks are needed!")
    print("==========================================================")
end
