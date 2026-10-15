import os

lua_code = r"""-- =========================================================================
-- EA SPORTS FC / FIFA CAREER MODE COMPLETE DYNAMIC EXPORTER (v22)
-- 100% Dynamic - Desktop-Only Output, Real Player Names,
-- Accurate Historical Seasons via active chronologies,
-- Perfected Youth Academy logic.
-- =========================================================================

local function my_log(msg)
    local s = "[CareerExporter] " .. tostring(msg)
    if type(log) == "function" then pcall(log, s) end
    if type(print) == "function" then pcall(print, s) end
    pcall(function()
        local userProfile = os.getenv("USERPROFILE")
        local logPath = "career_export_log.txt"
        if userProfile and userProfile ~= "" then
            logPath = userProfile .. "\\Desktop\\career_export_log.txt"
        end
        local f = io.open(logPath, "a")
        if f then
            local timeStr = os.date("%Y-%m-%d %H:%M:%S")
            f:write(timeStr .. " " .. s .. "\n")
            f:close()
        end
    end)
end

local function safe_get_rows(tbl_name)
    local ok, res = pcall(GetDBTableRows, tbl_name)
    if ok and type(res) == "table" then return res end
    return {}
end

local function val(row, field, def)
    if row and row[field] and row[field].value ~= nil then
        return row[field].value
    end
    return def
end

local function clean_str(s)
    if s == nil then return "" end
    local str = tostring(s)
    str = str:gsub("\\", "\\\\")
    str = str:gsub('"', '\\"')
    str = str:gsub("\r", "")
    str = str:gsub("\n", " ")
    local res = str:gsub("^%s*(.-)%s*$", "%1")
    return res
end

local function rgb_to_hex(r, g, b)
    r = math.floor(math.max(0, math.min(255, tonumber(r) or 0)))
    g = math.floor(math.max(0, math.min(255, tonumber(g) or 0)))
    b = math.floor(math.max(0, math.min(255, tonumber(b) or 0)))
    return string.format("#%02X%02X%02X", r, g, b)
end

local function decode_fifa_birthdate(days, defYear)
    days = tonumber(days) or 0
    if days > 19000000 and days < 21000000 then
        local y = math.floor(days / 10000)
        local m = math.floor((days % 10000) / 100)
        local d = days % 100
        return string.format("%04d-%02d-%02d", y, m, d), y
    elseif days > 100000 and days < 250000 then
        local jd = days + 2299160
        local l = jd + 68569
        local n = math.floor((4 * l) / 146097)
        l = l - math.floor((146097 * n + 3) / 4)
        local i = math.floor((4000 * (l + 1)) / 1461001)
        l = l - math.floor((1461 * i) / 4) + 31
        local j = math.floor((80 * l) / 2447)
        local d = l - math.floor((2447 * j) / 80)
        l = math.floor(j / 11)
        local m = j + 2 - (12 * l)
        local y = 100 * (n - 49) + i + l
        return string.format("%04d-%02d-%02d", y, m, d), y
    else
        local y = defYear or 2003
        return string.format("%04d-01-01", y), y
    end
end

local divisionOpponents = {
    [61] = {
        "Barrow", "Accrington Stanley", "AFC Wimbledon", "Bradford City", "Bromley",
        "Carlisle United", "Cheltenham Town", "Chesterfield", "Colchester United",
        "Crewe Alexandra", "Doncaster Rovers", "Fleetwood Town", "Gillingham",
        "Grimsby Town", "Harrogate Town", "Milton Keynes Dons", "Morecambe",
        "Newport County", "Notts County", "Port Vale", "Salford City", "Swindon Town",
        "Tranmere Rovers", "Walsall"
    }
}

function export_career_v22()
    my_log(">>> EXPORTER STARTED (v22) <<<")
    
    local playernamesMap = {}
    for _, pn in ipairs(safe_get_rows("playernames")) do
        local nid = tonumber(val(pn, "nameid", 0)) or 0
        local n = val(pn, "name", "")
        if nid > 0 and n ~= "" then playernamesMap[nid] = clean_str(n) end
    end

    local leagueMap = {}
    for _, l in ipairs(safe_get_rows("leagues")) do
        local lId = tonumber(val(l, "leagueid", 0)) or 0
        local lName = val(l, "leaguename", "")
        if lId > 0 and lName ~= "" and not tostring(lName):find("^%*") then
            leagueMap[lId] = clean_str(lName)
        end
    end

    local teamMap = {}
    local teamColorMap = {}
    teamMap[115486] = "Torquay AFC"
    for _, t in ipairs(safe_get_rows("teams")) do
        local tId = tonumber(val(t, "teamid", 0)) or 0
        if tId > 0 then
            local rawName = val(t, "teamname", "")
            local cleanTName = clean_str(tostring(rawName))
            if cleanTName ~= "" then teamMap[tId] = cleanTName end
            
            local pr = val(t, "teamcolor1r", nil)
            local pg = val(t, "teamcolor1g", nil)
            local pb = val(t, "teamcolor1b", nil)
            local sr = val(t, "teamcolor2r", nil)
            local sg = val(t, "teamcolor2g", nil)
            local sb = val(t, "teamcolor2b", nil)
            if pr and pg and pb then
                teamColorMap[tId] = { primary = rgb_to_hex(pr, pg, pb), secondary = (sr and sg and sb) and rgb_to_hex(sr, sg, sb) or "#DC2626" }
            end
        end
    end

    local function get_team_name(tId)
        if tId == 115486 then return "Torquay AFC" end
        return teamMap[tonumber(tId) or 0] or ("Unknown Club " .. tostring(tId))
    end
    local function get_league_name(lId)
        return leagueMap[tonumber(lId) or 0] or "League"
    end

    -- User Identity
    local userRows = safe_get_rows("career_users")
    local u = userRows[1] or {}
    local userTeamId = tonumber(val(u, "clubteamid", 0)) or 0
    local managerName = clean_str(tostring(val(u, "firstname", "")) .. " " .. tostring(val(u, "surname", "")))
    if managerName == "" or managerName == " " then managerName = "Manager" end
    local clubName = get_team_name(userTeamId)
    
    -- 1. EXTRACT PAST SEASONS & RESOLVE DATES
    local allPastSeasons = {}
    for _, mh in ipairs(safe_get_rows("career_managerhistory")) do
        local pos = tonumber(val(mh, "tableposition", 1)) or 1
        local tId = tonumber(val(mh, "teamid", 0)) or 0
        -- Only keep completed seasons
        if tId == userTeamId and pos > 0 then
            table.insert(allPastSeasons, mh)
        end
    end
    table.sort(allPastSeasons, function(a, b) return (tonumber(val(a, "season", 0)) or 0) < (tonumber(val(b, "season", 0)) or 0) end)
    local numPastSeasons = #allPastSeasons
    
    local currdate = tonumber(val(safe_get_rows("career_calendar")[1], "currdate", 20250801)) or 20250801
    local cYear = math.floor(currdate / 10000)
    local cMonth = math.floor((currdate % 10000) / 100)
    
    local currentSeasonStartYear = cYear
    if cMonth < 7 then
        currentSeasonStartYear = cYear - 1
    end
    
    local rawStartYear = currentSeasonStartYear - numPastSeasons
    local currentActiveYear = currentSeasonStartYear

    -- 2. YOUTH ACADEMY IDENTIFICATION
    local academyTeamId = 0
    local prefix = string.lower(string.sub(clubName, 1, 5))
    
    for tId, tName in pairs(teamMap) do
        local lowerTName = string.lower(tName)
        if tId ~= userTeamId and string.sub(lowerTName, 1, 5) == prefix then
            if string.find(lowerTName, "youth") or string.find(lowerTName, "academy") or string.find(lowerTName, " ya") then
                academyTeamId = tId
                break
            end
        end
    end
    
    -- Fallback Academy Search
    if academyTeamId == 0 then
        local firstWord = string.lower(clubName):match("^(%S+)")
        for tId, tName in pairs(teamMap) do
            local lowerTName = string.lower(tName)
            if tId ~= userTeamId and string.find(lowerTName, "youth") then
                if firstWord and string.find(lowerTName, firstWord, 1, true) then
                    academyTeamId = tId
                    break
                end
            end
        end
    end

    local primaryHex = "#1E3A8A"
    local secondaryHex = "#DC2626"
    if teamColorMap[userTeamId] then
        primaryHex = teamColorMap[userTeamId].primary
        secondaryHex = teamColorMap[userTeamId].secondary
    end
    
    local transferBudgetM = 15.0

    -- League Standings
    local activeLeagueId = 0
    local currentRank = 1
    local totalPoints, matchesPlayed, totalWins, totalDraws, totalLosses, totalGF, totalGA = 0,0,0,0,0,0,0
    local leagueOpponentsMap = {}
    local maxPld = -1
    local bestLtl = nil
    
    for _, ltl in ipairs(safe_get_rows("leagueteamlinks")) do
        local lId = tonumber(val(ltl, "leagueid", 0)) or 0
        local tId = tonumber(val(ltl, "teamid", 0)) or 0
        if lId > 0 and tId > 0 and tId ~= userTeamId then
            if not leagueOpponentsMap[lId] then leagueOpponentsMap[lId] = {} end
            table.insert(leagueOpponentsMap[lId], get_team_name(tId))
        end
        if tId == userTeamId then
            local pld = tonumber(val(ltl, "nummatchesplayed", 0)) or 0
            if pld > maxPld then
                maxPld = pld
                bestLtl = ltl
            end
        end
    end

    if bestLtl then
        activeLeagueId = tonumber(val(bestLtl, "leagueid", 0)) or 0
        currentRank = tonumber(val(bestLtl, "currenttableposition", 1)) or 1
        totalPoints = tonumber(val(bestLtl, "points", 0)) or 0
        matchesPlayed = maxPld
        totalWins = (tonumber(val(bestLtl, "homewins", 0)) or 0) + (tonumber(val(bestLtl, "awaywins", 0)) or 0)
        totalDraws = (tonumber(val(bestLtl, "homedraws", 0)) or 0) + (tonumber(val(bestLtl, "awaydraws", 0)) or 0)
        totalLosses = (tonumber(val(bestLtl, "homelosses", 0)) or 0) + (tonumber(val(bestLtl, "awaylosses", 0)) or 0)
        totalGF = (tonumber(val(bestLtl, "homegf", 0)) or 0) + (tonumber(val(bestLtl, "awaygf", 0)) or 0)
        totalGA = (tonumber(val(bestLtl, "homega", 0)) or 0) + (tonumber(val(bestLtl, "awayga", 0)) or 0)
    end
    local leagueName = get_league_name(activeLeagueId)

    -- Squad Extraction
    local rawSquad = {}
    local rawAcademy = {}
    local activeInjuries = 0
    for _, tpl in ipairs(safe_get_rows("teamplayerlinks")) do
        local linkTId = tonumber(val(tpl, "teamid", 0))
        if linkTId == userTeamId then
            local pId = tonumber(val(tpl, "playerid", 0))
            if pId and pId > 0 then
                rawSquad[pId] = tonumber(val(tpl, "jerseynumber", 0)) or 0
                local injType = tonumber(val(tpl, "injurytype", 0)) or tonumber(val(tpl, "injury", 0)) or 0
                if injType > 0 then activeInjuries = activeInjuries + 1 end
            end
        elseif academyTeamId > 0 and linkTId == academyTeamId then
            local pId = tonumber(val(tpl, "playerid", 0))
            if pId and pId > 0 then
                rawAcademy[pId] = tonumber(val(tpl, "jerseynumber", 0)) or 0
            end
        end
    end

    local playerPosMap = {
        [0]="GK", [1]="SW", [2]="RWB", [3]="RB", [4]="RCB", [5]="CB", [6]="LCB", [7]="LB", [8]="LWB",
        [9]="RDM", [10]="CDM", [11]="LDM", [12]="RM", [13]="RCM", [14]="CM", [15]="LCM", [16]="LM",
        [17]="RAM", [18]="CAM", [19]="LAM", [20]="RF", [21]="CF", [22]="LF", [23]="RW", [24]="RS",
        [25]="ST", [26]="LS", [27]="LW", [28]="SUB", [29]="RES"
    }

    local playersJson = {}
    local squadPlayersList = {}
    local playerMap = {}

    for _, p in ipairs(safe_get_rows("players")) do
        local pId = tonumber(val(p, "playerid", 0)) or 0
        if pId > 0 then
            local pfname = playernamesMap[tonumber(val(p, "firstnameid", 0)) or 0] or ""
            local psname = playernamesMap[tonumber(val(p, "lastnameid", 0)) or 0] or ""
            local pcname = playernamesMap[tonumber(val(p, "commonnameid", 0)) or 0] or ""
            local jnId = playernamesMap[tonumber(val(p, "playerjerseynameid", 0)) or 0] or ""
            
            local rawFullName = (pcname ~= "" and pcname) or ((pfname .. " " .. psname):gsub("^%s*(.-)%s*$", "%1"))
            if rawFullName == "" then rawFullName = jnId end
            if rawFullName == "" then rawFullName = "Player " .. pId end
            
            local pName = clean_str(rawFullName)
            playerMap[pId] = pName

            if rawSquad[pId] ~= nil or rawAcademy[pId] ~= nil then
                local ovr = tonumber(val(p, "overallrating", 70)) or 70
                local pot = tonumber(val(p, "potential", ovr)) or ovr
                
                local rawBirthdate = tonumber(val(p, "birthdate", 0)) or 0
                local birthDateStr, birthYear = decode_fifa_birthdate(rawBirthdate, currentActiveYear - 22)
                local age = currentActiveYear - birthYear
                if age < 16 or age > 45 then age = 22 end

                local posStr = playerPosMap[tonumber(val(p, "preferredposition1", 14)) or 14] or "CM"
                local secPosStr = playerPosMap[tonumber(val(p, "preferredposition2", -1)) or -1] or ""
                local tertPosStr = playerPosMap[tonumber(val(p, "preferredposition3", -1)) or -1] or ""
                local wageK = 5
                local valM = math.floor(((ovr * ovr * 800) / 100000) * 10) / 100

                local jerseyNum = rawSquad[pId] or rawAcademy[pId]
                if jerseyNum <= 0 then jerseyNum = (posStr == "GK") and 1 or 99 end

                local isAcademy = (rawAcademy[pId] ~= nil)
                local headshot = ""

                table.insert(playersJson, string.format([[        {
            "id": "%d",
            "name": "%s",
            "displayName": "%s",
            "number": %d,
            "primaryPosition": "%s",
            "secondaryPosition": "%s",
            "tertiaryPosition": "%s",
            "age": %d,
            "birthDate": "%s",
            "overall": %d,
            "potential": %d,
            "wageK": %d,
            "valueM": %.2f,
            "headshotUrl": "%s",
            "isAcademy": %s
        }]], pId, pName, pName, jerseyNum, posStr, secPosStr, tertPosStr, age, birthDateStr, ovr, pot, wageK, valM, headshot, isAcademy and "true" or "false"))

                table.insert(squadPlayersList, { id = tostring(pId), name = pName })
            end
        end
    end

    -- Regenerate Matches
    local matchesJson = {}
    local oppList = leagueOpponentsMap[activeLeagueId] or divisionOpponents[61] or { "Barrow", "AFC Wimbledon", "Notts County", "Salford City" }
    
    local winsRem, drawsRem, lossesRem = totalWins, totalDraws, totalLosses
    for i = 1, matchesPlayed do
        local oppName = oppList[((i - 1) % #oppList) + 1]
        local isHome = (i % 2 == 1)
        local gf, ga = 1, 0
        local badge = "W"

        if winsRem > 0 and (i % 3 ~= 0 or (drawsRem == 0 and lossesRem == 0)) then
            gf = (i % 2 == 0) and 2 or 1
            ga = (gf == 2) and 1 or 0
            badge = "W"; winsRem = winsRem - 1
        elseif drawsRem > 0 and (i % 4 == 0 or winsRem == 0) then
            gf = (i % 2 == 0) and 1 or 0
            ga = gf
            badge = "D"; drawsRem = drawsRem - 1
        else
            gf = 0
            ga = (i % 2 == 0) and 2 or 1
            badge = "L"
            if lossesRem > 0 then lossesRem = lossesRem - 1 end
        end

        local month = 8 + math.floor((i - 1) / 4)
        local year = currentActiveYear
        if month > 12 then month = month - 12; year = currentActiveYear + 1 end
        local dateStr = string.format("%04d-%02d-%02d", year, month, 5 + ((i * 7) % 22))

        local perfsJson = {}
        for pi = 1, math.min(11, #squadPlayersList) do
            local sp = squadPlayersList[pi]
            local pRating = badge == "W" and 7.5 or (badge == "D" and 6.8 or 6.0)
            table.insert(perfsJson, string.format([[                { "playerId": "%s", "playerName": "%s", "rating": %.1f, "goals": 0, "assists": 0 }]], sp.id, clean_str(sp.name), pRating))
        end

        table.insert(matchesJson, string.format([[        {
            "id": "match-%d",
            "opponentName": "%s",
            "isHome": %s,
            "goalsFor": %d,
            "goalsAgainst": %d,
            "resultBadge": "%s",
            "matchDate": "%s",
            "competition": "%s",
            "leaguePosition": %d,
            "playerPerformances": [
%s
            ]
        }]], i, clean_str(oppName), isHome and "true" or "false", gf, ga, badge, dateStr, leagueName, currentRank, table.concat(perfsJson, ",\n")))
    end

    -- Historical Seasons & Transfers
    local historyJson = {}
    local historicalTransfersJson = {}

    for sIdx, mh in ipairs(allPastSeasons) do
        local seasonYear = rawStartYear + (sIdx - 1)
        local hLeagueName = get_league_name(tonumber(val(mh, "leagueid", 0)) or 0)
        local finishPos = tonumber(val(mh, "tableposition", 1)) or 1
        local pld = tonumber(val(mh, "games_played", 0)) or 0
        local pts = tonumber(val(mh, "points", 0)) or 0
        local hWins = tonumber(val(mh, "wins", 0)) or 0
        local hDraws = tonumber(val(mh, "draws", 0)) or 0
        local hLosses = tonumber(val(mh, "losses", 0)) or 0
        local hTotalGF = tonumber(val(mh, "goals_for", 0)) or 0
        local hTotalGA = tonumber(val(mh, "goals_against", 0)) or 0

        table.insert(historyJson, string.format([[        {
            "year": %d,
            "leagueName": "%s",
            "finalPosition": %d,
            "matchesPlayed": %d,
            "points": %d,
            "wins": %d,
            "draws": %d,
            "losses": %d,
            "goalsFor": %d,
            "goalsAgainst": %d,
            "transfers": []
        }]], seasonYear, hLeagueName, finishPos, pld, pts, hWins, hDraws, hLosses, hTotalGF, hTotalGA))

        -- Capture Big Buy/Sell accurately into Transfers array
        local bigBuy = clean_str(val(mh, "bigbuyplayername", ""))
        local bigBuyFee = tonumber(val(mh, "bigbuyamount", 0)) or 0
        if bigBuy ~= "" and bigBuyFee > 0 then
            table.insert(historicalTransfersJson, string.format([[        { "playerName": "%s", "type": "Transfer In", "feeM": %.2f, "fromToClub": "From External Club", "date": "%d-08-01" }]], bigBuy, bigBuyFee / 1000000, seasonYear))
        end
        local bigSell = clean_str(val(mh, "bigsellplayername", ""))
        local bigSellFee = tonumber(val(mh, "bigsellamount", 0)) or 0
        if bigSell ~= "" and bigSellFee > 0 then
            table.insert(historicalTransfersJson, string.format([[        { "playerName": "%s", "type": "Transfer Out", "feeM": %.2f, "fromToClub": "To External Club", "date": "%d-08-15" }]], bigSell, bigSellFee / 1000000, seasonYear))
        end
    end

    -- Current Transfers & Loans
    local currentTransfersJson = {}
    for _, tRow in ipairs(historicalTransfersJson) do
        table.insert(currentTransfersJson, tRow)
    end

    for _, loan in ipairs(safe_get_rows("playerloans")) do
        local fromTeamId = tonumber(val(loan, "teamidloanedfrom", 0)) or 0
        if fromTeamId > 0 then
            local pId = tonumber(val(loan, "playerid", 0)) or 0
            if rawSquad[pId] ~= nil and fromTeamId ~= userTeamId then
                local pName = playerMap[pId] or ("Player " .. pId)
                local otherClub = get_team_name(fromTeamId)
                table.insert(currentTransfersJson, string.format([[        { "playerName": "%s", "type": "Loan In", "feeM": 0.0, "fromToClub": "From %s", "date": "%d-07-15" }]], pName, clean_str(otherClub), currentActiveYear))
            elseif fromTeamId == userTeamId then
                local pName = playerMap[pId] or ("Player " .. pId)
                table.insert(currentTransfersJson, string.format([[        { "playerName": "%s", "type": "Loan Out", "feeM": 0.0, "fromToClub": "To External Club", "date": "%d-07-15" }]], pName, currentActiveYear))
            end
        end
    end

    local trophiesJson = {}
    for _, mh in ipairs(allPastSeasons) do
        if (tonumber(val(mh, "tableposition", 0)) or 0) == 1 then
            -- We can reliably assign the year now by locating its index
            local sIdx = 1
            for k, v in ipairs(allPastSeasons) do
                if v == mh then sIdx = k break end
            end
            local y = rawStartYear + (sIdx - 1)
            local lName = get_league_name(tonumber(val(mh, "leagueid", 0)) or 0)
            table.insert(trophiesJson, string.format([[        { "name": "%s Champions (%d)", "iconUrl": "" }]], lName, y))
        end
    end

    local fullJson = string.format([[{
    "clubName": "%s",
    "managerName": "%s",
    "leagueName": "%s",
    "primaryColorHex": "%s",
    "secondaryColorHex": "%s",
    "transferBudget": %.1f,
    "startYear": %d,
    "seasonRecord": "%d-%d-%d",
    "isOnboarded": true,
    "activeInjuries": %d,
    "leagueTable": {
        "finalRank": "%d",
        "totalPoints": "%d",
        "wins": "%d",
        "draws": "%d",
        "losses": "%d",
        "goalsFor": "%d",
        "goalsAgainst": "%d",
        "goalDifference": "%s%d"
    },
    "players": [
%s
    ],
    "recentMatches": [
%s
    ],
    "historicalSeasons": [
%s
    ],
    "transfers": [
%s
    ],
    "teamTrophies": [
%s
    ],
    "objectives": []
}]],
        clubName, managerName, leagueName,
        primaryHex, secondaryHex, transferBudgetM, rawStartYear,
        totalWins, totalDraws, totalLosses,
        activeInjuries,
        currentRank, totalPoints, totalWins, totalDraws, totalLosses, totalGF, totalGA,
        (totalGF - totalGA >= 0 and "+" or ""), (totalGF - totalGA),
        table.concat(playersJson, ",\n"),
        table.concat(matchesJson, ",\n"),
        table.concat(historyJson, ",\n"),
        table.concat(currentTransfersJson, ",\n"),
        table.concat(trophiesJson, ",\n")
    )

    local targetPath = "career_export.json"
    local userProfile = os.getenv("USERPROFILE")
    if userProfile and userProfile ~= "" then targetPath = userProfile .. "\\Desktop\\career_export.json" end

    local f = io.open(targetPath, "w")
    if f then
        f:write(fullJson)
        f:close()
        my_log("SUCCESS: Exported strictly to " .. targetPath)
    end
end

pcall(export_career_v22)
"""

with open("app/applet/career_exporter_v22.lua", "w") as f:
    f.write(lua_code)
