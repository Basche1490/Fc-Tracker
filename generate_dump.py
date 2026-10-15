# Script to update dump_match_data.lua to inspect career_playerinfo and find all tables containing Torquay United

dump_code = r'''-- =========================================================================
-- EA SPORTS FC / FIFA - DUMP MATCH & FIXTURE DATA (Comprehensive Scanner)
-- Scans every table in the DB for Torquay United (115486), dumps player stats,
-- manager history, and all fixture/calendar details into Desktop log.
-- =========================================================================

local function my_log(msg)
    local s = "[DumpMatchData] " .. tostring(msg)
    pcall(print, s)
    pcall(function()
        local userProfile = os.getenv("USERPROFILE") or ""
        local logPath = (userProfile ~= "") and (userProfile .. "\\Desktop\\telemetry_sync_log.txt") or "telemetry_sync_log.txt"
        local f = io.open(logPath, "a")
        if f then
            f:write(os.date("%Y-%m-%d %H:%M:%S") .. " " .. s .. "\n")
            f:close()
        end
    end)
end

local function safe_get_rows(tbl_name)
    local ok, res = pcall(GetDBTableRows, tbl_name)
    if ok and type(res) == "table" then return res end
    return {}
end

local function raw_val(innerVal)
    if innerVal == nil then return nil end
    if type(innerVal) == "table" then
        if innerVal.value ~= nil then return innerVal.value end
        if innerVal[1] ~= nil then return innerVal[1] end
    end
    if type(innerVal) == "userdata" then
        local ok, uv = pcall(function() return innerVal.value end)
        if ok and uv ~= nil then return uv end
    end
    return innerVal
end

local function get_field(row, colName)
    if not row or colName == nil then return nil end
    local v = raw_val(row[colName])
    if v ~= nil then return v end
    local targetLower = tostring(colName):lower()
    for k, valItem in pairs(row) do
        if tostring(k):lower() == targetLower then
            return raw_val(valItem)
        end
    end
    return nil
end

local function dump_all()
    my_log("=================================================================")
    my_log(">>> STARTING DEEP SCAN: FINDING ALL MATCH & TORQUAY DATA <<<")
    my_log("=================================================================")

    local userTeamId = 115486
    local userClubName = "Torquay United"

    -- 1. Inspect 'career_managerhistory'
    local mhRows = safe_get_rows("career_managerhistory")
    my_log(string.format("TABLE 'career_managerhistory': Total Rows = %d", #mhRows))
    for i, row in ipairs(mhRows) do
        local parts = {}
        for k, v in pairs(row) do
            local rv = raw_val(v)
            if rv ~= nil and tostring(rv) ~= "" then
                table.insert(parts, string.format("%s=%s", tostring(k), tostring(rv)))
            end
        end
        my_log(string.format("  ManagerHistory[%d]: %s", i, table.concat(parts, " | ")))
    end

    -- 2. Inspect 'career_playerinfo' for Torquay United's squad
    local squadPids = {}
    for _, tpl in ipairs(safe_get_rows("teamplayerlinks")) do
        local tid = tonumber(get_field(tpl, "teamid")) or 0
        local pid = tonumber(get_field(tpl, "playerid")) or 0
        if tid == userTeamId and pid > 0 then
            squadPids[pid] = true
        end
    end

    local piRows = safe_get_rows("career_playerinfo")
    my_log(string.format("TABLE 'career_playerinfo': Total Rows = %d", #piRows))
    local userPiCount = 0
    if #piRows > 0 then
        local firstRow = piRows[1]
        local colList = {}
        for k, _ in pairs(firstRow) do table.insert(colList, tostring(k)) end
        table.sort(colList)
        my_log("TABLE 'career_playerinfo' Columns: " .. table.concat(colList, ", "))

        for _, pi in ipairs(piRows) do
            local pid = tonumber(get_field(pi, "playerid")) or 0
            if squadPids[pid] then
                userPiCount = userPiCount + 1
                local parts = {}
                for _, colName in ipairs(colList) do
                    local v = raw_val(pi[colName])
                    if v ~= nil and tostring(v) ~= "" and tostring(v) ~= "0" and tostring(v) ~= "-1" then
                        table.insert(parts, string.format("%s=%s", colName, tostring(v)))
                    end
                end
                my_log(string.format("  PlayerInfo[pId=%d]: %s", pid, table.concat(parts, " | ")))
            end
        end
    end
    my_log(string.format("Found %d Torquay United players in 'career_playerinfo'", userPiCount))

    -- 3. SCAN ALL KNOWN TABLES IN DB TO SEE WHICH TABLES CONTAIN 115486!
    local allTablesToScan = {
        "fixtures", "matchresults", "schedule", "matchschedule", "roundfixtures",
        "tournamentfixtures", "calendar", "competition_fixtures", "career_match",
        "career_fixtures", "career_results", "career_schedule", "career_calendar",
        "career_playerinfo", "standings", "competitions", "leagueteamlinks",
        "career_managerhistory", "teamplayerlinks", "career_users", "teams",
        "leagues", "players", "career_transferhistory", "playerloans",
        "career_boardobjectives", "youthplayers", "createdteams", "editedteamnames",
        "manager", "managers", "stadiums", "career_managerinfo", "career_squadranking"
    }

    if type(GetDBTableNames) == "function" then
        local ok, allT = pcall(GetDBTableNames)
        if ok and type(allT) == "table" and #allT > 0 then
            allTablesToScan = allT
        end
    end

    my_log("--- SCANNING FOR ANY OTHER TABLE CONTAINING TORQUAY (ID 115486) ---")
    local tablesWithTorquay = {}
    for _, tName in ipairs(allTablesToScan) do
        local rows = safe_get_rows(tName)
        if #rows > 0 and tName ~= "teams" and tName ~= "career_users" and tName ~= "teamplayerlinks" then
            local matchCount = 0
            local sampleRow = nil
            for _, r in ipairs(rows) do
                for k, v in pairs(r) do
                    if tonumber(raw_val(v)) == userTeamId then
                        matchCount = matchCount + 1
                        if not sampleRow then sampleRow = r end
                    end
                end
            end
            if matchCount > 0 then
                table.insert(tablesWithTorquay, string.format("%s (%d rows)", tName, matchCount))
                local parts = {}
                for k, v in pairs(sampleRow) do
                    local rv = raw_val(v)
                    if rv ~= nil and tostring(rv) ~= "" and tostring(rv) ~= "0" and tostring(rv) ~= "-1" then
                        table.insert(parts, string.format("%s=%s", tostring(k), tostring(rv)))
                    end
                end
                my_log(string.format("  Table '%s' contains Torquay in %d rows! Sample: %s", tName, matchCount, table.concat(parts, " | ")))
            end
        end
    end
    my_log("All Tables Containing Torquay United: " .. table.concat(tablesWithTorquay, " , "))

    my_log("=================================================================")
    my_log(">>> DEEP SCAN COMPLETE! Check Desktop telemetry_sync_log.txt <<<")
    my_log("=================================================================")
    print("[DumpMatchData ⚡ COMPLETE] Check your Desktop/telemetry_sync_log.txt for full scan results!")
end

pcall(dump_all)
'''

with open("app/applet/dump_match_data.lua", "w", encoding="utf-8") as f:
    f.write(dump_code)
print("dump_match_data.lua updated!")
