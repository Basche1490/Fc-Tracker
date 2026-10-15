-- =========================================================================
-- EA SPORTS FC / FIFA - MATCH DATA INSPECTOR & DIAGNOSTIC SCANNER
-- Run this in Live Editor to see exactly what the game stores for your club
-- =========================================================================

local function my_log(msg)
    local s = "[MatchInspector] " .. tostring(msg)
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

local function run_inspection()
    my_log("=================================================================")
    my_log(">>> MATCH DATA & CAREER MODE DIAGNOSTIC INSPECTION <<<")
    my_log("=================================================================")

    -- 1. Check Native Live Editor APIs
    local inCM = "N/A"
    if type(IsInCM) == "function" then
        local ok, res = pcall(IsInCM)
        if ok then inCM = tostring(res) end
    end

    local apiTeamId = 0
    if type(GetUserTeamID) == "function" then
        local ok, res = pcall(GetUserTeamID)
        if ok and tonumber(res) then apiTeamId = tonumber(res) end
    end

    local apiDate = "N/A"
    if type(GetCurrentDate) == "function" then
        local ok, res = pcall(GetCurrentDate)
        if ok and res ~= nil then apiDate = tostring(res) end
    end

    my_log(string.format("Live Editor APIs -> IsInCM: %s | GetUserTeamID: %d | GetCurrentDate: %s", inCM, apiTeamId, apiDate))

    -- 2. Detect User Team
    local userTeamId = apiTeamId
    if userTeamId == 0 then
        for _, u in ipairs(safe_get_rows("career_users")) do
            local uid = tonumber(get_field(u, "clubteamid")) or tonumber(get_field(u, "teamid")) or tonumber(get_field(u, "userteamid")) or 0
            if uid > 0 then userTeamId = uid; break end
        end
    end
    if userTeamId == 0 then userTeamId = 115486 end -- Torquay fallback

    -- Team Name Resolution
    local teamMap = {}
    for _, t in ipairs(safe_get_rows("teams")) do
        local tid = tonumber(get_field(t, "teamid")) or 0
        local tname = get_field(t, "teamname")
        if tid > 0 and tname and tname ~= "" then teamMap[tid] = tostring(tname) end
    end
    for _, ct in ipairs(safe_get_rows("createdteams")) do
        local tid = tonumber(get_field(ct, "teamid")) or 0
        local cname = get_field(ct, "teamname") or get_field(ct, "customteamname") or get_field(ct, "clubname")
        if tid > 0 and cname and cname ~= "" then teamMap[tid] = tostring(cname) end
    end
    for _, etn in ipairs(safe_get_rows("editedteamnames")) do
        local tid = tonumber(get_field(etn, "teamid")) or 0
        local ename = get_field(etn, "teamname") or get_field(etn, "customteamname")
        if tid > 0 and ename and ename ~= "" then teamMap[tid] = tostring(ename) end
    end

    local function resolve_team(tid)
        return teamMap[tid] or ("Team " .. tostring(tid))
    end

    local clubName = resolve_team(userTeamId)
    if clubName == ("Team " .. tostring(userTeamId)) then clubName = "Torquay United" end
    my_log(string.format("Target Club: %s (ID: %d)", clubName, userTeamId))

    -- 3. Check in-game calendar
    local calRows = safe_get_rows("career_calendar")
    my_log(string.format("TABLE career_calendar: %d rows", #calRows))
    if #calRows > 0 then
        local firstCal = calRows[1]
        local parts = {}
        for k, v in pairs(firstCal) do
            local rv = raw_val(v)
            if rv ~= nil then table.insert(parts, string.format("%s=%s", tostring(k), tostring(rv))) end
        end
        my_log("  career_calendar[1]: " .. table.concat(parts, " | "))
    end

    -- 4. Check leagueteamlinks for userTeamId
    local ltlRows = safe_get_rows("leagueteamlinks")
    my_log(string.format("TABLE leagueteamlinks: Total Rows = %d", #ltlRows))
    local userLtlCount = 0
    for _, ltl in ipairs(ltlRows) do
        local tid = tonumber(get_field(ltl, "teamid")) or 0
        if tid == userTeamId then
            userLtlCount = userLtlCount + 1
            local parts = {}
            local colKeys = {}
            for k, _ in pairs(ltl) do table.insert(colKeys, tostring(k)) end
            table.sort(colKeys)
            for _, k in ipairs(colKeys) do
                local rv = raw_val(ltl[k])
                if rv ~= nil then table.insert(parts, string.format("%s=%s", k, tostring(rv))) end
            end
            my_log(string.format("  League Standings Row[%d]: %s", userLtlCount, table.concat(parts, " | ")))
        end
    end
    if userLtlCount == 0 then
        my_log(string.format("  WARNING: userTeamId %d was NOT found in leagueteamlinks!", userTeamId))
    end

    -- 5. Check career_managerhistory
    local mhRows = safe_get_rows("career_managerhistory")
    my_log(string.format("TABLE career_managerhistory: Total Rows = %d", #mhRows))
    local userMhCount = 0
    for _, mh in ipairs(mhRows) do
        local tid = tonumber(get_field(mh, "teamid")) or 0
        if tid == userTeamId or tid == 0 or #mhRows <= 5 then
            userMhCount = userMhCount + 1
            local parts = {}
            local colKeys = {}
            for k, _ in pairs(mh) do table.insert(colKeys, tostring(k)) end
            table.sort(colKeys)
            for _, k in ipairs(colKeys) do
                local rv = raw_val(mh[k])
                if rv ~= nil then table.insert(parts, string.format("%s=%s", k, tostring(rv))) end
            end
            my_log(string.format("  Manager Record[%d]: %s", userMhCount, table.concat(parts, " | ")))
        end
    end

    -- 6. Check upcoming fixtures for user club
    local fixRows = safe_get_rows("fixtures")
    my_log(string.format("TABLE fixtures: Total Rows = %d", #fixRows))
    local userFixCount = 0
    for i, fix in ipairs(fixRows) do
        local hid = tonumber(get_field(fix, "hometeamid")) or 0
        local aid = tonumber(get_field(fix, "awayteamid")) or 0
        if hid == userTeamId or aid == userTeamId then
            userFixCount = userFixCount + 1
            local isHome = (hid == userTeamId)
            local oppId = isHome and aid or hid
            local oppName = resolve_team(oppId)
            local fixDate = tonumber(get_field(fix, "fixturedate")) or 0
            local compId = tonumber(get_field(fix, "competitionid")) or 0
            my_log(string.format("  Upcoming Match[%d]: %s vs %s (Date: %d, CompID: %d)",
                userFixCount, isHome and clubName or oppName, isHome and oppName or clubName, fixDate, compId))
        end
    end
    if userFixCount == 0 then
        my_log("  NOTE: No upcoming fixtures in the immediate window for Torquay United.")
    end

    -- 7. Check Player Stats in career_playerinfo
    local squadPids = {}
    for _, tpl in ipairs(safe_get_rows("teamplayerlinks")) do
        local tid = tonumber(get_field(tpl, "teamid")) or 0
        local pid = tonumber(get_field(tpl, "playerid")) or 0
        if tid == userTeamId and pid > 0 then squadPids[pid] = true end
    end

    local piRows = safe_get_rows("career_playerinfo")
    my_log(string.format("TABLE career_playerinfo: %d rows (Squad size in links: %d)", #piRows, userFixCount))
    local activePlayersWithStats = 0
    for _, pi in ipairs(piRows) do
        local pid = tonumber(get_field(pi, "playerid")) or 0
        if squadPids[pid] then
            local apps = tonumber(get_field(pi, "appearances")) or tonumber(get_field(pi, "leagueappearances")) or 0
            local goals = tonumber(get_field(pi, "goals")) or tonumber(get_field(pi, "leaguegoals")) or 0
            local assists = tonumber(get_field(pi, "assists")) or tonumber(get_field(pi, "leagueassists")) or 0
            if apps > 0 or goals > 0 or assists > 0 then
                activePlayersWithStats = activePlayersWithStats + 1
                my_log(string.format("  Player[ID=%d]: Apps=%d, Goals=%d, Assists=%d", pid, apps, goals, assists))
            end
        end
    end
    my_log(string.format("Active Torquay players with non-zero match stats: %d", activePlayersWithStats))

    my_log("=================================================================")
    my_log(">>> INSPECTION COMPLETE! Check Desktop telemetry_sync_log.txt <<<")
    my_log("=================================================================")
end

pcall(run_inspection)
