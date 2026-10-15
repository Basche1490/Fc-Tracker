# Generator for telemetry_sync.lua v4.8 and send_latest_match.lua v4.8

sync_code = r'''-- =========================================================================
-- EA SPORTS FC LIVE TELEMETRY SYNC (v4.8 - Precision Transfers & Matches)
-- Supports Create-a-Club, League Matches, Cup Matches, Pre-Season & Transfers
-- =========================================================================

-- SET TO true TO FORCE-SEND THE MOST RECENT MATCH IMMEDIATELY ON RUN:
local FORCE_SYNC_LATEST = false

-- AUTO-SYNC CONFIGURATION:
local AUTO_SYNC = true
local AUTO_SYNC_INTERVAL_SEC = 3

local function my_log(msg)
    local s = "[TelemetrySync] " .. tostring(msg)
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

local function val(row, field, def)
    local v = get_field(row, field)
    if v ~= nil then return v end
    return def
end

local function escape_str(s)
    if s == nil then return "" end
    local str = tostring(s):gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\n", " "):gsub("\r", "")
    return str:gsub("^%s*(.-)%s*$", "%1")
end

local function decode_fifa_date(days, defYear)
    days = tonumber(days) or 0
    if days > 19000000 and days < 21000000 then
        local y = math.floor(days / 10000); local m = math.floor((days % 10000) / 100); local d = days % 100
        return string.format("%04d-%02d-%02d", y, m, d)
    elseif days > 100000 and days < 250000 then
        local jd = days + 2299160; local l = jd + 68569
        local n = math.floor((4 * l) / 146097); l = l - math.floor((146097 * n + 3) / 4)
        local i = math.floor((4000 * (l + 1)) / 1461001); l = l - math.floor((1461 * i) / 4) + 31
        local j = math.floor((80 * l) / 2447); local d = l - math.floor((2447 * j) / 80)
        l = math.floor(j / 11); local m = j + 2 - (12 * l); local y = 100 * (n - 49) + i + l
        return string.format("%04d-%02d-%02d", y, m, d)
    else
        return string.format("%04d-08-01", defYear or 2027)
    end
end

local function send_to_bridge(json_payload)
    local temp_dir = os.getenv("TEMP") or os.getenv("TMP") or "."
    local ts = tostring(os.time()) .. "_" .. tostring(math.random(1000, 9999))
    local temp_json = temp_dir .. "\\fifa_telemetry_payload_" .. ts .. ".json"
    local temp_bat = temp_dir .. "\\fifa_send_telemetry_" .. ts .. ".bat"
    
    local jf = io.open(temp_json, "wb")
    if jf then
        jf:write(json_payload)
        jf:close()
    end
    
    local bf = io.open(temp_bat, "w")
    if bf then
        bf:write(string.format([[@echo off
curl -s -X POST -H "Content-Type: application/json; charset=utf-8" --data-binary @"%s" http://127.0.0.1:5050 >nul 2>&1
if %%ERRORLEVEL%% NEQ 0 (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-RestMethod -Uri 'http://127.0.0.1:5050' -Method POST -ContentType 'application/json; charset=utf-8' -InFile '%s' } catch {}" >nul 2>&1
)
del "%s" >nul 2>&1
(goto) 2>nul & del "%%~f0" >nul 2>&1
]], temp_json, temp_json, temp_json))
        bf:close()
        os.execute(string.format('start /B "" "%s"', temp_bat))
        my_log("Dispatched payload to bridge (" .. tostring(#json_payload) .. " bytes)")
    end
end

function run_telemetry_sync(isAuto)
    if not isAuto then
        my_log(">>> RUNNING TELEMETRY SYNC V4.8 <<<")
    end
    
    local userProfile = os.getenv("USERPROFILE") or ""
    local statePath = (userProfile ~= "") and (userProfile .. "\\Desktop\\telemetry_state.lua") or "telemetry_state.lua"
    local candidateStatePaths = {
        userProfile .. "\\Desktop\\FC26-LE\\telemetry_state.lua",
        userProfile .. "\\Desktop\\telemetry_state.lua",
        "telemetry_state.lua"
    }
    for _, sp in ipairs(candidateStatePaths) do
        local sf = io.open(sp, "r")
        if sf then
            sf:close()
            statePath = sp
            break
        end
    end

    -- 1. Build lookup maps
    local playernamesMap = {}
    for _, pn in ipairs(safe_get_rows("playernames")) do
        local nid = tonumber(val(pn, "nameid", 0)) or 0
        local n = val(pn, "name", "")
        if nid > 0 and n ~= "" then playernamesMap[nid] = escape_str(n) end
    end

    local leagueMap = {}
    for _, l in ipairs(safe_get_rows("leagues")) do
        local lId = tonumber(val(l, "leagueid", 0)) or 0
        local lName = val(l, "leaguename", "")
        if lId > 0 and lName ~= "" and not tostring(lName):find("^%*") then leagueMap[lId] = escape_str(lName) end
    end

    local teamMap = {}
    for _, t in ipairs(safe_get_rows("teams")) do
        local tId = tonumber(val(t, "teamid", 0)) or 0
        local tName = val(t, "teamname", "")
        if tId > 0 and tName ~= "" and not tostring(tName):find("^%*") then
            teamMap[tId] = escape_str(tostring(tName))
        end
    end

    -- Created Clubs & Custom Team Names resolution (Create-a-Club mode)
    for _, ct in ipairs(safe_get_rows("createdteams")) do
        local tId = tonumber(val(ct, "teamid", 0)) or 0
        local cName = val(ct, "teamname", val(ct, "customteamname", val(ct, "clubname", "")))
        if tId > 0 and cName ~= "" and not tostring(cName):find("^%*") then
            teamMap[tId] = escape_str(tostring(cName))
        end
    end
    for _, etn in ipairs(safe_get_rows("editedteamnames")) do
        local tId = tonumber(val(etn, "teamid", 0)) or 0
        local cName = val(etn, "teamname", val(etn, "customteamname", ""))
        if tId > 0 and cName ~= "" and not tostring(cName):find("^%*") then
            teamMap[tId] = escape_str(tostring(cName))
        end
    end

    local function get_team_name(tId)
        local n = teamMap[tonumber(tId) or 0]
        if n and n ~= "" and not tostring(n):find("^%*") then return n end
        return "Team " .. tostring(tId)
    end

    -- Fast player lookup map
    local playersMap = {}
    for _, p in ipairs(safe_get_rows("players")) do
        local pid = tonumber(val(p, "playerid", 0)) or 0
        if pid > 0 then playersMap[pid] = p end
    end

    local function get_player_name(pId)
        local p = playersMap and playersMap[pId]
        if p then
            local pfname = val(p, "firstname", "")
            if pfname == "" then pfname = playernamesMap[tonumber(val(p, "firstnameid", 0)) or 0] or "" end
            local psname = val(p, "surname", "")
            if psname == "" then psname = val(p, "lastname", "") end
            if psname == "" then psname = playernamesMap[tonumber(val(p, "lastnameid", 0)) or 0] or "" end
            local pcname = val(p, "commonname", "")
            if pcname == "" then pcname = playernamesMap[tonumber(val(p, "commonnameid", 0)) or 0] or "" end
            
            local rawFullName = (pcname ~= "" and pcname) or ((pfname .. " " .. psname):gsub("^%s*(.-)%s*$", "%1"))
            if rawFullName == "" then rawFullName = psname ~= "" and psname or pfname end
            return escape_str(rawFullName)
        end
        return "Player " .. tostring(pId)
    end

    -- 2. Detect userTeamId
    local userTeamId = 0
    for _, u in ipairs(safe_get_rows("career_users")) do
        local uid = tonumber(val(u, "clubteamid", val(u, "teamid", val(u, "userteamid", 0)))) or 0
        if uid > 0 then
            userTeamId = uid
            break
        end
    end
    if userTeamId == 0 then
        for _, mh in ipairs(safe_get_rows("career_managerhistory")) do
            local tid = tonumber(val(mh, "teamid", 0)) or 0
            if tid > 0 then
                userTeamId = tid
                break
            end
        end
    end
    if userTeamId == 0 then userTeamId = 115486 end

    local userClubName = get_team_name(userTeamId)
    if tostring(userClubName):find("^%*") or tostring(userClubName):find("^Team ") or userClubName == "Unknown" then
        local u = safe_get_rows("career_users")[1]
        local cuName = val(u, "clubname", val(u, "teamname", ""))
        if cuName ~= "" and not tostring(cuName):find("^%*") then
            userClubName = escape_str(cuName)
        else
            userClubName = "Torquay United"
        end
        teamMap[userTeamId] = userClubName
    end

    -- 3. Resolve Current Calendar Date
    local currdate = 0
    for _, cal in ipairs(safe_get_rows("career_calendar")) do
        local d = tonumber(val(cal, "currdate", val(cal, "caldate", 0))) or 0
        if d > 20200000 then
            currdate = d
            break
        end
    end
    if currdate == 0 then
        currdate = 20270815
    end
    local cYear = math.floor(currdate / 10000)
    local cMonth = math.floor((currdate % 10000) / 100)
    local cDay = currdate % 100
    if cYear < 2020 or cMonth < 1 or cMonth > 12 or cDay < 1 or cDay > 31 then
        cYear = 2027
        cMonth = 8
        cDay = 15
    end
    local todayDateStr = string.format("%04d-%02d-%02d", cYear, cMonth, cDay)

    -- 4. Extract Squad & Player Stats
    local currentSquad = {}
    local currentPlayerStats = {}
    local playerToTeamMap = {}
    local totalSquadForm = 0
    local squadCount = 0

    for _, tpl in ipairs(safe_get_rows("teamplayerlinks")) do
        local tid = tonumber(val(tpl, "teamid", 0)) or 0
        local pId = tonumber(val(tpl, "playerid", 0)) or 0
        if pId > 0 and tid > 0 then
            playerToTeamMap[pId] = tid
            if tid == userTeamId then
                currentSquad[pId] = true
                squadCount = squadCount + 1
                local form = tonumber(val(tpl, "form", 3)) or 3
                totalSquadForm = totalSquadForm + form
                local estRating = 6.0 + (form * 0.5)
                if estRating > 9.5 then estRating = 9.5 end
                currentPlayerStats[pId] = { goals=0, assists=0, apps=0, yellows=0, reds=0, rating=estRating }
            end
        end
    end

    for _, pi in ipairs(safe_get_rows("career_playerinfo")) do
        local pId = tonumber(val(pi, "playerid", 0)) or 0
        if currentSquad[pId] then
            local apps = math.max(
                tonumber(val(pi, "appearances", 0)) or 0,
                tonumber(val(pi, "leagueappearances", 0)) or 0,
                tonumber(val(pi, "allappearances", 0)) or 0,
                tonumber(val(pi, "appearancescup", 0)) or 0,
                tonumber(val(pi, "appearancescontinental", 0)) or 0,
                tonumber(val(pi, "matchesplayed", 0)) or 0,
                tonumber(val(pi, "gamesplayed", 0)) or 0
            )
            local goals = math.max(
                tonumber(val(pi, "goals", 0)) or 0,
                tonumber(val(pi, "leaguegoals", 0)) or 0,
                tonumber(val(pi, "allgoals", 0)) or 0,
                tonumber(val(pi, "goalscup", 0)) or 0,
                tonumber(val(pi, "goalscontinental", 0)) or 0
            )
            local assists = math.max(
                tonumber(val(pi, "assists", 0)) or 0,
                tonumber(val(pi, "leagueassists", 0)) or 0,
                tonumber(val(pi, "allassists", 0)) or 0,
                tonumber(val(pi, "assistscup", 0)) or 0
            )
            local rating = tonumber(val(pi, "matchrating", 0)) or 0
            local yellows = math.max(
                tonumber(val(pi, "yellows", 0)) or 0,
                tonumber(val(pi, "yellowcards", 0)) or 0,
                tonumber(val(pi, "yellowcardsleague", 0)) or 0,
                tonumber(val(pi, "yellowcardscup", 0)) or 0
            )
            local reds = math.max(
                tonumber(val(pi, "reds", 0)) or 0,
                tonumber(val(pi, "redcards", 0)) or 0,
                tonumber(val(pi, "redcardsleague", 0)) or 0,
                tonumber(val(pi, "redcardscup", 0)) or 0
            )
            
            local prev = currentPlayerStats[pId] or {}
            currentPlayerStats[pId] = {
                goals = math.max(prev.goals or 0, goals),
                assists = math.max(prev.assists or 0, assists),
                apps = math.max(prev.apps or 0, apps),
                yellows = math.max(prev.yellows or 0, yellows),
                reds = math.max(prev.reds or 0, reds),
                rating = rating > 0 and rating or (prev.rating or 7.0)
            }
        end
    end

    -- 5. Extract League Stats
    local currentStats = { pld=0, hw=0, aw=0, hd=0, ad=0, hl=0, al=0, hgf=0, agf=0, hga=0, aga=0, leagueId=14 }
    local maxLeaguePld = -1
    local bestLtl = nil
    local totalUserLtls = 0

    for _, ltl in ipairs(safe_get_rows("leagueteamlinks")) do
        local tId = tonumber(val(ltl, "teamid", 0)) or 0
        if tId == userTeamId then
            totalUserLtls = totalUserLtls + 1
            local pld = tonumber(val(ltl, "nummatchesplayed", 0)) or 0
            local hw = tonumber(val(ltl, "homewins", 0)) or 0
            local aw = tonumber(val(ltl, "awaywins", 0)) or 0
            local hd = tonumber(val(ltl, "homedraws", 0)) or 0
            local ad = tonumber(val(ltl, "awaydraws", 0)) or 0
            local hl = tonumber(val(ltl, "homelosses", 0)) or 0
            local al = tonumber(val(ltl, "awaylosses", 0)) or 0
            local sumPld = hw + aw + hd + ad + hl + al
            if sumPld > pld then pld = sumPld end
            
            if pld > maxLeaguePld then
                maxLeaguePld = pld
                bestLtl = ltl
            end
        end
    end

    if bestLtl then
        currentStats.leagueId = tonumber(val(bestLtl, "leagueid", 14)) or 14
        currentStats.pld = maxLeaguePld
        currentStats.hw = tonumber(val(bestLtl, "homewins", 0)) or 0
        currentStats.aw = tonumber(val(bestLtl, "awaywins", 0)) or 0
        currentStats.hd = tonumber(val(bestLtl, "homedraws", 0)) or 0
        currentStats.ad = tonumber(val(bestLtl, "awaydraws", 0)) or 0
        currentStats.hl = tonumber(val(bestLtl, "homelosses", 0)) or 0
        currentStats.al = tonumber(val(bestLtl, "awaylosses", 0)) or 0
        currentStats.hgf = tonumber(val(bestLtl, "homegf", 0)) or 0
        currentStats.agf = tonumber(val(bestLtl, "awaygf", 0)) or 0
        currentStats.hga = tonumber(val(bestLtl, "homega", 0)) or 0
        currentStats.aga = tonumber(val(bestLtl, "awayga", 0)) or 0
    end

    -- 6. Parse Manager History & Big Buys
    -- Sort rows by season descending so the latest season is picked
    local allMhRows = safe_get_rows("career_managerhistory")
    local bigBuysMap = {}
    local currManagerMatches = 0
    local currManagerWins = 0
    local currManagerDraws = 0
    local currManagerLosses = 0
    local currManagerGF = 0
    local currManagerGA = 0
    local allTimeManagerMatches = 0
    local latestSeasonNum = 0

    for _, mh in ipairs(allMhRows) do
        local bName = val(mh, "bigbuyplayername", "")
        local bAmt = tonumber(val(mh, "bigbuyamount", 0)) or 0
        if bName ~= "" and bAmt > 0 then
            bigBuysMap[tostring(bName):lower()] = bAmt / 1000000
        end

        local tId = tonumber(val(mh, "teamid", 0)) or 0
        if tId == userTeamId then
            local sNum = tonumber(val(mh, "season", 0)) or 0
            local gp = tonumber(val(mh, "games_played", val(mh, "matchesplayed", 0))) or 0
            local w = tonumber(val(mh, "wins", 0)) or 0
            local d = tonumber(val(mh, "draws", 0)) or 0
            local l = tonumber(val(mh, "losses", 0)) or 0
            local gf = tonumber(val(mh, "goals_for", 0)) or 0
            local ga = tonumber(val(mh, "goals_against", 0)) or 0
            if gp == 0 and (w + d + l > 0) then gp = w + d + l end

            allTimeManagerMatches = allTimeManagerMatches + gp

            if sNum >= latestSeasonNum then
                latestSeasonNum = sNum
                currManagerMatches = gp
                currManagerWins = w
                currManagerDraws = d
                currManagerLosses = l
                currManagerGF = gf
                currManagerGA = ga
            end
        end
    end

    -- 7. Load Previous State
    local state = nil
    local sf = io.open(statePath, "r")
    if sf then
        sf:close()
        local ok, res = pcall(dofile, statePath)
        if ok and type(res) == "table" then state = res end
    end

    if state then
        state.squad = state.squad or {}
        state.playerStats = state.playerStats or {}
        state.allPlayerTeams = state.allPlayerTeams or {}
    end

    -- Calculate squad performance deltas
    local totalAppsNow, totalAppsPrev = 0, 0
    local totalGoalsNow, totalGoalsPrev = 0, 0
    local totalCardsNow, totalCardsPrev = 0, 0
    for pId, pStats in pairs(currentPlayerStats) do
        totalAppsNow = totalAppsNow + (pStats.apps or 0)
        totalGoalsNow = totalGoalsNow + (pStats.goals or 0)
        totalCardsNow = totalCardsNow + (pStats.yellows or 0) + (pStats.reds or 0)
        local prevStats = (state and state.playerStats and state.playerStats[pId]) or {apps=0, goals=0, yellows=0, reds=0}
        totalAppsPrev = totalAppsPrev + (prevStats.apps or 0)
        totalGoalsPrev = totalGoalsPrev + (prevStats.goals or 0)
        totalCardsPrev = totalCardsPrev + (prevStats.yellows or 0) + (prevStats.reds or 0)
    end
    local appsDiffTotal = totalAppsNow - totalAppsPrev
    local goalsDiffTotal = totalGoalsNow - totalGoalsPrev
    local cardsDiffTotal = totalCardsNow - totalCardsPrev

    -- Calculate deltas
    local leagueMatchDiff = (state and state.pld) and (currentStats.pld - state.pld) or 0
    local managerDiff = (state and state.currManagerMatches) and (currManagerMatches - state.currManagerMatches) or 0
    local allTimeManagerDiff = (state and state.allTimeManagerMatches) and (allTimeManagerMatches - state.allTimeManagerMatches) or 0

    if not isAuto then
        my_log(string.format("Club: %s (ID: %d) | Season: %d | Date: %s | Squad: %d", userClubName, userTeamId, latestSeasonNum, todayDateStr, squadCount))
        my_log(string.format("League Links: Matches=%d | Latest Season Manager: %d Matches (W:%d D:%d L:%d | GF:%d GA:%d)",
            currentStats.pld, currManagerMatches, currManagerWins, currManagerDraws, currManagerLosses, currManagerGF, currManagerGA))
        my_log(string.format("Deltas -> League: +%d | ManagerSeason: +%d | Apps: +%d | Goals: +%d",
            leagueMatchDiff, managerDiff, appsDiffTotal, goalsDiffTotal))
    end

    local matchTriggered = false
    local triggerReason = "None"

    if FORCE_SYNC_LATEST then
        matchTriggered = true
        triggerReason = "FORCE_SYNC_LATEST manual override"
    elseif leagueMatchDiff > 0 then
        matchTriggered = true
        triggerReason = string.format("League Matches Delta (+%d matches)", leagueMatchDiff)
    elseif managerDiff > 0 then
        matchTriggered = true
        triggerReason = string.format("Manager Season Delta (+%d matches)", managerDiff)
    elseif allTimeManagerDiff > 0 then
        matchTriggered = true
        triggerReason = string.format("Manager History Delta (+%d matches)", allTimeManagerDiff)
    elseif appsDiffTotal > 0 or goalsDiffTotal > 0 or cardsDiffTotal > 0 then
        matchTriggered = true
        triggerReason = string.format("Squad Performance Delta (Apps: +%d, Goals: +%d, Cards: +%d)", appsDiffTotal, goalsDiffTotal, cardsDiffTotal)
    end

    if matchTriggered then
        my_log(">>> MATCH DETECTED! Reason: " .. triggerReason .. " <<<")

        local oppName = "League Opponent"
        local isHome = true
        local gf, ga = 2, 1
        local badge = "W"
        local competitionName = leagueMap[currentStats.leagueId] or "Championship"
        local isCup = false
        local isET = false
        local homePens = 0
        local awayPens = 0
        local stageName = "Matchday " .. math.max(1, currentStats.pld > 0 and currentStats.pld or (currManagerMatches > 0 and currManagerMatches or 1))

        local prevW = state and state.currManagerWins or 0
        local prevD = state and state.currManagerDraws or 0
        local prevL = state and state.currManagerLosses or 0
        local prevGF = state and state.currManagerGF or 0
        local prevGA = state and state.currManagerGA or 0

        if currManagerWins > prevW then
            badge = "W"
            gf = math.max(1, currManagerGF - prevGF)
            ga = math.max(0, currManagerGA - prevGA)
        elseif currManagerLosses > prevL then
            badge = "L"
            gf = math.max(0, currManagerGF - prevGF)
            ga = math.max(1, currManagerGA - prevGA)
        elseif currManagerDraws > prevD then
            badge = "D"
            gf = math.max(0, currManagerGF - prevGF)
            ga = gf
        else
            gf = math.max(1, goalsDiffTotal)
            ga = 0
            badge = "W"
        end

        -- Build Player Performances & Goal Details
        local matchPerfsStr = ""
        local matchGoalsStr = ""
        local addedGoals = false
        local addedPerfs = false
        local perfIndex = 0
        local topPlayerName = ""
        local topScore = -1

        local squadList = {}
        for pId, _ in pairs(currentSquad) do table.insert(squadList, pId) end
        table.sort(squadList)

        for _, pId in ipairs(squadList) do
            local pStats = currentPlayerStats[pId]
            local prevStats = (state and state.playerStats and state.playerStats[pId]) or {goals=0, assists=0, apps=0, rating=7.0}
            local appsDiff = (pStats and pStats.apps or 0) - prevStats.apps
            local goalsDiff = (pStats and pStats.goals or 0) - prevStats.goals
            local assistsDiff = (pStats and pStats.assists or 0) - prevStats.assists

            if appsDiff > 0 or goalsDiff > 0 or assistsDiff > 0 or (perfIndex < 11 and #squadList <= 18) then
                perfIndex = perfIndex + 1
                local pName = get_player_name(pId)
                local pRating = math.min(9.9, math.max(6.0, 7.0 + goalsDiff * 0.8 + assistsDiff * 0.5 + (perfIndex % 3) * 0.2))
                
                local pScore = goalsDiff * 3 + assistsDiff * 2 + pRating
                if pScore > topScore then
                    topScore = pScore
                    topPlayerName = pName
                end

                local perfBlock = string.format(
                    '{"playerId":"%d","playerName":"%s","goals":%d,"assists":%d,"rating":%.1f,"passes":%d,"passAccuracy":%d,"shots":%d,"shotAccuracy":%d,"saves":0,"penaltySaves":0,"tackles":%d,"tacklePercentage":80,"interceptions":1,"cleanSheet":%s,"yellowCard":false,"redCard":false,"isMotm":false}',
                    pId, pName, goalsDiff, assistsDiff, pRating, 35 + (perfIndex * 3) % 20, 85 + (perfIndex % 8), goalsDiff + (perfIndex % 2), (goalsDiff > 0) and 75 or 0, 2 + (perfIndex % 3), (ga == 0) and "true" or "false"
                )
                if addedPerfs then matchPerfsStr = matchPerfsStr .. "," else addedPerfs = true end
                matchPerfsStr = matchPerfsStr .. perfBlock
            end
        end

        for g = 1, gf do
            local scorerName = topPlayerName ~= "" and topPlayerName or userClubName .. " Striker"
            if squadList[g] then scorerName = get_player_name(squadList[g]) end
            local min = 15 + ((g * 28) % 70)
            local gBlock = string.format('{"playerName":"%s","minute":%d,"isOpponent":false}', scorerName, min)
            if addedGoals then matchGoalsStr = matchGoalsStr .. "," else addedGoals = true end
            matchGoalsStr = matchGoalsStr .. gBlock
        end
        for g = 1, ga do
            local min = 20 + ((g * 31) % 65)
            local gBlock = string.format('{"playerName":"%s (Opponent)","minute":%d,"isOpponent":true}', oppName, min)
            if addedGoals then matchGoalsStr = matchGoalsStr .. "," else addedGoals = true end
            matchGoalsStr = matchGoalsStr .. gBlock
        end

        local shotsF = math.max(gf + 3, math.floor(gf * 3.2 + 4))
        local shotsA = math.max(ga + 2, math.floor(ga * 3.0 + 3))
        local xGF = math.floor((gf * 0.82 + 0.35) * 100) / 100
        local xGA = math.floor((ga * 0.78 + 0.28) * 100) / 100
        local poss = isHome and (gf >= ga and 56 or 50) or (gf >= ga and 52 or 46)

        local locMsg = isHome and "vs" or "@"
        local title = isCup and "Cup Match Final" or "Live Match Final"
        local msg = string.format("Full Time: %s %d - %d %s (%s)", locMsg, gf, ga, oppName, competitionName)

        local payload = string.format(
            '{"dataType":"match","title":"%s","message":"%s","opponentName":"%s","isHome":%s,"goalsFor":%d,"goalsAgainst":%d,"resultBadge":"%s","date":"%s","competition":"%s","stage":"%s","isExtraTime":%s,"homePenalties":%d,"awayPenalties":%d,"possession":%d,"passingAccuracy":88,"shotsFor":%d,"shotsAgainst":%d,"expectedGoals":%.2f,"expectedGoalsAgainst":%.2f,"leaguePosition":%d,"motmName":"%s","playerPerformances":[%s],"goalDetails":[%s]}',
            title, msg, oppName, isHome and "true" or "false", gf, ga, badge, todayDateStr, competitionName, stageName, isET and "true" or "false", homePens, awayPens, poss, shotsF, shotsA, xGF, xGA, 1, topPlayerName, matchPerfsStr, matchGoalsStr
        )

        send_to_bridge(payload)
        my_log(">>> SENT MATCH RESULT: " .. msg)
        pcall(print, string.format("[TelemetrySync ⚡ MATCH SYNCED] %s", msg))
    else
        if not isAuto then
            my_log("No new matches detected since last sync.")
            my_log("TIP: Click 'Advance' after a match so stats save, or run 'send_latest_match.lua' to beam latest match instantly!")
        end
    end

    -- 8. PRECISION TRANSFER LOGIC
    for pId, _ in pairs(currentSquad) do
        if state and state.squad and not state.squad[pId] then
            local pName = get_player_name(pId)
            local feeM = 0.0
            local transferType = "Transfer In"
            local fromClub = ""
            
            -- Step A: Did this player come from a specific team?
            local prevTid = (state.allPlayerTeams and state.allPlayerTeams[pId]) or playerToTeamMap[pId] or 0
            if prevTid > 0 and prevTid ~= userTeamId then
                fromClub = get_team_name(prevTid)
            end

            -- Step B: If player came from another club, preserve that club name!
            local cameFromAnotherClub = (fromClub ~= "" and fromClub ~= "External Club" and not tostring(fromClub):find("^Team ") and fromClub ~= userClubName)

            if cameFromAnotherClub then
                transferType = "Transfer In"
                -- Check if this player matches bigbuyplayername in career_managerhistory
                for bNameLower, bFee in pairs(bigBuysMap) do
                    if pName:lower():find(bNameLower, 1, true) or bNameLower:find(pName:lower(), 1, true) then
                        feeM = bFee
                        break
                    end
                end
                -- If no fee is found, set to 0.0 as requested
            else
                -- Not from an external club: check if Youth Academy
                local p = playersMap[pId]
                local isAcad = false
                if p then
                    local isAcadField = tonumber(val(p, "isacademy", 0)) or 0
                    if isAcadField == 1 or pId >= 300000 then isAcad = true end
                elseif pId >= 300000 then
                    isAcad = true
                end

                if isAcad then
                    fromClub = "Youth Academy"
                    transferType = "Promoted In"
                    feeM = 0.0
                else
                    fromClub = "External Club"
                    transferType = "Transfer In"
                    feeM = 0.0
                end
            end

            -- Step C: Resolve Exact Transfer Date from playerjointeamdate
            local transferDateStr = todayDateStr
            local p = playersMap[pId]
            if p then
                local joinDays = tonumber(val(p, "playerjointeamdate", 0)) or 0
                if joinDays > 0 then
                    transferDateStr = decode_fifa_date(joinDays, cYear)
                end
            end

            local msg = string.format("%s joined from %s!", pName, fromClub)
            local payload = string.format(
                '{"dataType":"transfer","title":"Transfer Alert","message":"%s","playerName":"%s","type":"%s","feeM":%.2f,"fromToClub":"%s","date":"%s"}',
                msg, pName, transferType, feeM, fromClub, transferDateStr
            )
            send_to_bridge(payload)
            my_log(string.format("Sent Transfer In: %s (From: %s | Fee: £%.2fM | Date: %s)", pName, fromClub, feeM, transferDateStr))
            pcall(print, string.format("[TelemetrySync ⚡ TRANSFER IN] %s (From: %s | £%.2fM | %s)", pName, fromClub, feeM, transferDateStr))
        end
    end

    for pId, _ in pairs(state and state.squad or {}) do
        if not currentSquad[pId] then
            local pName = get_player_name(pId)
            local toClub = "External Club"
            local newTid = playerToTeamMap[pId]
            if newTid and newTid > 0 and newTid ~= userTeamId then
                toClub = get_team_name(newTid)
            else
                toClub = "Free Agent / Released"
            end

            local msg = string.format("%s transferred to %s.", pName, toClub)
            local payload = string.format(
                '{"dataType":"transfer","title":"Transfer Alert","message":"%s","playerName":"%s","type":"Transfer Out","feeM":0.0,"fromToClub":"%s","date":"%s"}',
                msg, pName, toClub, todayDateStr
            )
            send_to_bridge(payload)
            my_log(string.format("Sent Transfer Out: %s (To: %s)", pName, toClub))
            pcall(print, string.format("[TelemetrySync ⚡ TRANSFER OUT] %s", msg))
        end
    end

    -- 9. Save New State
    local squadDump = "{"
    for pId, _ in pairs(currentSquad) do squadDump = squadDump .. "[" .. pId .. "]=true," end
    squadDump = squadDump .. "}"

    local pStatsDump = "{"
    for pId, ps in pairs(currentPlayerStats) do
        pStatsDump = pStatsDump .. string.format("[%d]={goals=%d, assists=%d, apps=%d, yellows=%d, reds=%d},", pId, ps.goals, ps.assists, ps.apps, ps.yellows or 0, ps.reds or 0)
    end
    pStatsDump = pStatsDump .. "}"

    local allTeamsDump = "{"
    for pId, tId in pairs(playerToTeamMap) do allTeamsDump = allTeamsDump .. string.format("[%d]=%d,", pId, tId) end
    allTeamsDump = allTeamsDump .. "}"

    local outf = io.open(statePath, "w")
    if outf then
        outf:write(string.format([[
return {
    pld = %d, hw = %d, aw = %d, hd = %d, ad = %d, hl = %d, al = %d,
    hgf = %d, agf = %d, hga = %d, aga = %d,
    currdate = %d,
    currManagerMatches = %d,
    currManagerWins = %d,
    currManagerDraws = %d,
    currManagerLosses = %d,
    currManagerGF = %d,
    currManagerGA = %d,
    allTimeManagerMatches = %d,
    latestSeasonNum = %d,
    squad = %s,
    playerStats = %s,
    allPlayerTeams = %s
}
]], currentStats.pld, currentStats.hw, currentStats.aw, currentStats.hd, currentStats.ad, currentStats.hl, currentStats.al,
    currentStats.hgf, currentStats.agf, currentStats.hga, currentStats.aga,
    currdate,
    currManagerMatches,
    currManagerWins,
    currManagerDraws,
    currManagerLosses,
    currManagerGF,
    currManagerGA,
    allTimeManagerMatches,
    latestSeasonNum,
    squadDump, pStatsDump, allTeamsDump))
        outf:close()
        if not isAuto then
            my_log("State saved successfully.")
        end
    end
end

-- Run sync immediately
local ok, err = pcall(function() run_telemetry_sync(false) end)
if not ok then
    my_log("CRITICAL ERROR: " .. tostring(err))
    print("[TelemetrySync ERROR] " .. tostring(err))
end

-- Background timer registration if available in this Live Editor build
if AUTO_SYNC then
    if _G.FIFA_TELEMETRY_TIMER then
        pcall(function()
            if type(_G.FIFA_TELEMETRY_TIMER.destroy) == "function" then
                _G.FIFA_TELEMETRY_TIMER.destroy()
            elseif type(_G.FIFA_TELEMETRY_TIMER.setEnabled) == "function" then
                _G.FIFA_TELEMETRY_TIMER.setEnabled(false)
            end
        end)
        _G.FIFA_TELEMETRY_TIMER = nil
    end

    local timerCreated = false
    if type(createTimer) == "function" then
        local okTimer, t = pcall(function()
            local timer = createTimer(nil)
            timer.Interval = AUTO_SYNC_INTERVAL_SEC * 1000
            timer.OnTimer = function() pcall(function() run_telemetry_sync(true) end) end
            return timer
        end)
        if okTimer and t then
            _G.FIFA_TELEMETRY_TIMER = t
            timerCreated = true
        end
    end

    if timerCreated then
        print("[TelemetrySync] Background polling active (every 3s).")
    else
        print("=========================================================================")
        print(" [READY] EA FC LIVE TELEMETRY SYNC ACTIVE (v4.8)!")
        print(" Whenever you finish a match or make transfers:")
        print(" 1. Click 'Advance' on the post-match screen to return to Central Hub.")
        print(" 2. In Live Editor, tap 'Run' on telemetry_sync.lua (or hotkey F9)!")
        print(" 3. TIP: Run 'send_latest_match.lua' to beam your latest match immediately!")
        print("=========================================================================")
    end
end
'''

with open("app/applet/telemetry_sync.lua", "w", encoding="utf-8") as f:
    f.write(sync_code)
print("telemetry_sync.lua v4.8 written successfully!")
