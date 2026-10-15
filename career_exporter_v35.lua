-- =========================================================================
-- EA SPORTS FC 24/25/26 CAREER MODE COMPLETE DYNAMIC EXPORTER (v35)
-- Fixed Season Boundaries (July 1st) & Refined Regen Promotion Logic
-- =========================================================================

local function my_log(msg)
    local s = "[CareerExporter] " .. tostring(msg)
    pcall(function()
        local userProfile = os.getenv("USERPROFILE")
        local logPath = "career_export_log.txt"
        if userProfile and userProfile ~= "" then logPath = userProfile .. "\\Desktop\\career_export_log.txt" end
        local f = io.open(logPath, "a")
        if f then f:write(os.date("%Y-%m-%d %H:%M:%S") .. " " .. s .. "\n"); f:close() end
    end)
end

local function safe_get_rows(tbl_name)
    local ok, res = pcall(GetDBTableRows, tbl_name)
    if ok and type(res) == "table" then return res end
    return {}
end

local function val(row, field, def)
    if row and row[field] and row[field].value ~= nil then return row[field].value end
    return def
end

local function clean_str(s)
    if s == nil then return "" end
    local str = tostring(s):gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\r", ""):gsub("\n", " ")
    return str:gsub("^%s*(.-)%s*$", "%1")
end

local function decode_fifa_date(days, defYear)
    days = tonumber(days) or 0
    if days > 19000000 and days < 21000000 then
        local y = math.floor(days / 10000); local m = math.floor((days % 10000) / 100); local d = days % 100
        return string.format("%04d-%02d-%02d", y, m, d), y
    elseif days > 100000 and days < 250000 then
        local jd = days + 2299160; local l = jd + 68569
        local n = math.floor((4 * l) / 146097); l = l - math.floor((146097 * n + 3) / 4)
        local i = math.floor((4000 * (l + 1)) / 1461001); l = l - math.floor((1461 * i) / 4) + 31
        local j = math.floor((80 * l) / 2447); local d = l - math.floor((2447 * j) / 80)
        l = math.floor(j / 11); local m = j + 2 - (12 * l); local y = 100 * (n - 49) + i + l
        return string.format("%04d-%02d-%02d", y, m, d), y
    else
        return string.format("%04d-01-01", defYear or 2003), defYear or 2003
    end
end

function export_career_v35()
    my_log(">>> EXPORTER STARTED (v35) <<<")
    
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
        if lId > 0 and lName ~= "" and not tostring(lName):find("^%*") then leagueMap[lId] = clean_str(lName) end
    end

    local teamMap = {}
    for _, t in ipairs(safe_get_rows("teams")) do
        local tId = tonumber(val(t, "teamid", 0)) or 0
        if tId > 0 then
            local cleanTName = clean_str(tostring(val(t, "teamname", "")))
            if cleanTName ~= "" then teamMap[tId] = cleanTName end
        end
    end

    local defaultNations = {
        [1]="Albania", [2]="Algeria", [4]="Andorra", [5]="Angola", [6]="Antigua and Barbuda",
        [7]="Argentina", [8]="Armenia", [9]="Australia", [10]="Austria", [11]="Azerbaijan",
        [13]="Bahrain", [14]="England", [15]="Barbados", [16]="Belarus", [17]="Belgium",
        [18]="France", [19]="Bermuda", [20]="Bolivia", [21]="Germany", [22]="Bosnia and Herzegovina",
        [25]="Bulgaria", [26]="Burkina Faso", [27]="Italy", [28]="Cameroon", [29]="Canada",
        [30]="Cape Verde", [32]="Central African Republic", [33]="Chad", [34]="Netherlands",
        [35]="China PR", [36]="Chinese Taipei", [37]="Colombia", [38]="Portugal", [39]="Comoros",
        [40]="Congo", [41]="DR Congo", [42]="Scotland", [43]="Costa Rica", [44]="Ivory Coast",
        [45]="Spain", [46]="Cuba", [47]="Cyprus", [48]="Czech Republic", [49]="Denmark",
        [51]="Ecuador", [52]="Argentina", [53]="Egypt", [54]="Brazil", [55]="El Salvador",
        [56]="Equatorial Guinea", [57]="Chile", [58]="Colombia", [59]="Estonia", [60]="Croatia",
        [61]="Faroe Islands", [62]="Fiji", [63]="Finland", [64]="France", [65]="Gabon",
        [66]="Gambia", [67]="Georgia", [68]="Ghana", [69]="Greece", [70]="Grenada",
        [71]="Guatemala", [72]="Guinea", [73]="Guinea-Bissau", [74]="Guyana", [75]="Haiti",
        [76]="Honduras", [77]="Hong Kong", [78]="Hungary", [79]="Iceland", [80]="India",
        [81]="Indonesia", [82]="Iran", [83]="Iraq", [84]="Israel", [86]="Jamaica",
        [87]="Japan", [88]="Jordan", [89]="Kazakhstan", [90]="Kenya", [91]="Korea DPR",
        [92]="Korea Republic", [93]="Kosovo", [94]="Kuwait", [95]="United States", [96]="Latvia",
        [97]="Lebanon", [98]="Lesotho", [99]="Liberia", [100]="Libya", [101]="Liechtenstein",
        [102]="Lithuania", [103]="Luxembourg", [105]="Madagascar", [106]="Malawi", [107]="Malaysia",
        [108]="Maldives", [109]="Mali", [110]="Malta", [111]="Mauritania", [112]="Mauritius",
        [113]="Mexico", [114]="Moldova", [115]="Monaco", [116]="Mongolia", [117]="Montenegro",
        [118]="Montserrat", [119]="Morocco", [120]="Mozambique", [121]="Namibia", [123]="Nepal",
        [125]="New Zealand", [126]="Nicaragua", [127]="Niger", [128]="Nigeria", [129]="North Macedonia",
        [130]="Northern Ireland", [131]="Norway", [132]="Oman", [133]="Pakistan", [134]="Palestine",
        [135]="Panama", [136]="Papua New Guinea", [137]="Paraguay", [138]="Peru", [139]="Philippines",
        [140]="Poland", [141]="Portugal", [142]="Puerto Rico", [143]="Qatar", [144]="Republic of Ireland",
        [145]="Romania", [146]="Russia", [147]="Rwanda", [148]="Saint Kitts and Nevis", [149]="Saint Lucia",
        [150]="Saint Vincent and the Grenadines", [152]="San Marino", [153]="Sao Tome and Principe",
        [154]="Saudi Arabia", [155]="Senegal", [156]="Serbia", [157]="Seychelles", [158]="Sierra Leone",
        [159]="Singapore", [160]="Slovakia", [161]="Slovenia", [163]="Somalia", [164]="South Africa",
        [165]="South Sudan", [166]="Sri Lanka", [167]="Sudan", [168]="Suriname", [169]="Sweden",
        [170]="Switzerland", [171]="Syria", [172]="Tahiti", [173]="Tajikistan", [174]="Tanzania",
        [175]="Thailand", [176]="Timor-Leste", [177]="Togo", [178]="Tonga", [179]="Trinidad and Tobago",
        [180]="Tunisia", [181]="Turkey", [182]="Turkmenistan", [183]="Uganda", [184]="Ukraine",
        [185]="United Arab Emirates", [186]="Uruguay", [187]="Uzbekistan", [188]="Vanuatu",
        [189]="Venezuela", [190]="Vietnam", [191]="Wales", [192]="Yemen", [193]="Zambia", [194]="Zimbabwe"
    }

    local nationMap = {}
    for _, n in ipairs(safe_get_rows("nations")) do
        local nId = tonumber(val(n, "nationid", 0)) or 0
        local nName = val(n, "nationname", "")
        if nName == "" then nName = val(n, "name", "") end
        if nName == "" then
            local nNameId = tonumber(val(n, "nationnameid", 0)) or 0
            if nNameId > 0 and playernamesMap[nNameId] then nName = playernamesMap[nNameId] end
        end
        if nId > 0 and nName ~= "" and not tostring(nName):find("^%*") then
            nationMap[nId] = clean_str(nName)
        end
    end

    local function get_nation_name(nId)
        local n = tonumber(nId) or 0
        if n <= 0 then return "Unknown" end
        return nationMap[n] or defaultNations[n] or ("Nation " .. tostring(n))
    end

    local function get_team_name(tId)
        local tName = teamMap[tonumber(tId) or 0]
        if tName and string.find(tName, "^%*TeamName") then return "My Custom Club" end
        return tName or ("Unknown Club " .. tostring(tId))
    end
    local function get_league_name(lId) return leagueMap[tonumber(lId) or 0] or "League" end

    local userRows = safe_get_rows("career_users")
    local u = userRows[1] or {}
    local userTeamId = tonumber(val(u, "clubteamid", 0)) or 0
    local managerName = clean_str(tostring(val(u, "firstname", "")) .. " " .. tostring(val(u, "surname", "")))
    if managerName == "" or managerName == " " then managerName = "Manager" end
    local clubName = get_team_name(userTeamId)
    
    local primaryHex = "#1E3A8A"
    local secondaryHex = "#DC2626"
    local youthTeamId = 0
    local userTeamRawName = ""
    
    for _, t in ipairs(safe_get_rows("teams")) do
        local tid = tonumber(val(t, "teamid", 0)) or 0
        if tid == userTeamId then
            userTeamRawName = tostring(val(t, "teamname", ""))
            local r1, g1, b1 = tonumber(val(t, "teamcolor1r", -1)) or -1, tonumber(val(t, "teamcolor1g", -1)) or -1, tonumber(val(t, "teamcolor1b", -1)) or -1
            if r1 >= 0 and g1 >= 0 and b1 >= 0 then primaryHex = string.format("#%02X%02X%02X", r1, g1, b1) end
            local r2, g2, b2 = tonumber(val(t, "teamcolor2r", -1)) or -1, tonumber(val(t, "teamcolor2g", -1)) or -1, tonumber(val(t, "teamcolor2b", -1)) or -1
            if r2 >= 0 and g2 >= 0 and b2 >= 0 then secondaryHex = string.format("#%02X%02X%02X", r2, g2, b2) end
            break
        end
    end

    if string.find(userTeamRawName, "%*TeamName_Abbr") then
        local prefixMatch = string.match(userTeamRawName, "^(%*TeamName_Abbr%d+_)")
        if prefixMatch then
            for _, t in ipairs(safe_get_rows("teams")) do
                local tid = tonumber(val(t, "teamid", 0)) or 0
                if tid ~= userTeamId and string.sub(tostring(val(t, "teamname", "")), 1, string.len(prefixMatch)) == prefixMatch then
                    youthTeamId = tid; break
                end
            end
        end
    end
    
    local currdate = tonumber(val(safe_get_rows("career_calendar")[1], "currdate", 20250801)) or 20250801
    local cYear = math.floor(currdate / 10000)
    local cMonth = math.floor((currdate % 10000) / 100)
    local currentActiveYear = cMonth < 7 and (cYear - 1) or cYear
    if currentActiveYear < 2020 then currentActiveYear = 2025 + (#safe_get_rows("career_managerhistory") - 1) end

    local allPastSeasons = {}
    for _, mh in ipairs(safe_get_rows("career_managerhistory")) do
        local pos = tonumber(val(mh, "tableposition", 1)) or 1
        local tId = tonumber(val(mh, "teamid", 0)) or 0
        if tId == userTeamId and pos > 0 then table.insert(allPastSeasons, mh) end
    end
    table.sort(allPastSeasons, function(a, b) return (tonumber(val(a, "season", 0)) or 0) < (tonumber(val(b, "season", 0)) or 0) end)
    
    local rawStartYear = currentActiveYear - #allPastSeasons
    local transferBudgetM = 15.0

    local activeLeagueId, currentRank, matchesPlayed, maxPld = 0, 1, 0, -1
    local totalPoints, totalWins, totalDraws, totalLosses, totalGF, totalGA = 0,0,0,0,0,0
    local leagueOpponentsMap = {}
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
            if pld > maxPld then maxPld = pld; bestLtl = ltl end
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

    local rawSquad, rawYouth, activeInjuries = {}, {}, 0
    for _, tpl in ipairs(safe_get_rows("teamplayerlinks")) do
        local tid = tonumber(val(tpl, "teamid", 0)) or 0
        local pId = tonumber(val(tpl, "playerid", 0)) or 0
        if pId > 0 then
            if tid == userTeamId then
                rawSquad[pId] = tonumber(val(tpl, "jerseynumber", 0)) or 0
                local injType = tonumber(val(tpl, "injurytype", 0)) or tonumber(val(tpl, "injury", 0)) or 0
                if injType > 0 then activeInjuries = activeInjuries + 1 end
            elseif youthTeamId > 0 and tid == youthTeamId then
                rawYouth[pId] = tonumber(val(tpl, "jerseynumber", 0)) or 0
            end
        end
    end
    for _, yp in ipairs(safe_get_rows("youthplayers")) do
        if tonumber(val(yp, "teamid", 0)) == userTeamId then
            local pId = tonumber(val(yp, "playerid", 0)) or 0
            if pId > 0 then rawYouth[pId] = tonumber(val(yp, "jerseynumber", 0)) or 0 end
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
    local currentSeasonSigningsJson = {}
    
    local function get_player_name_from_id(pId)
        for _, p in ipairs(safe_get_rows("players")) do
            if tonumber(val(p, "playerid", 0)) == pId then
                local pfname = val(p, "firstname", "")
                if pfname == "" then pfname = playernamesMap[tonumber(val(p, "firstnameid", 0)) or 0] or "" end
                local psname = val(p, "surname", "")
                if psname == "" then psname = val(p, "lastname", "") end
                if psname == "" then psname = playernamesMap[tonumber(val(p, "lastnameid", 0)) or 0] or "" end
                local pcname = val(p, "commonname", "")
                if pcname == "" then pcname = playernamesMap[tonumber(val(p, "commonnameid", 0)) or 0] or "" end
                local jnId = playernamesMap[tonumber(val(p, "playerjerseynameid", 0)) or 0] or ""
                
                local rawFullName = (pcname ~= "" and pcname) or ((pfname .. " " .. psname):gsub("^%s*(.-)%s*$", "%1"))
                if rawFullName == "" then rawFullName = jnId end
                if rawFullName == "" then rawFullName = psname ~= "" and psname or pfname end
                return clean_str(rawFullName)
            end
        end
        return "Player " .. tostring(pId)
    end

    for _, p in ipairs(safe_get_rows("players")) do
        local pId = tonumber(val(p, "playerid", 0)) or 0
        if pId > 0 and (rawSquad[pId] ~= nil or rawYouth[pId] ~= nil) then
            local pName = get_player_name_from_id(pId)
            local ovr = tonumber(val(p, "overallrating", 70)) or 70
            local pot = tonumber(val(p, "potential", ovr)) or ovr
            
            local birthDateStr, birthYear = decode_fifa_date(tonumber(val(p, "birthdate", 0)) or 0, currentActiveYear - 22)
            local age = currentActiveYear - birthYear
            if age < 15 or age > 45 then age = 22 end

            local posStr = playerPosMap[tonumber(val(p, "preferredposition1", 14)) or 14] or "CM"
            local secPosStr = playerPosMap[tonumber(val(p, "preferredposition2", -1)) or -1] or ""
            local tertPosStr = playerPosMap[tonumber(val(p, "preferredposition3", -1)) or -1] or ""
            
            local jerseyNum = rawSquad[pId] or rawYouth[pId]
            if jerseyNum <= 0 then jerseyNum = (posStr == "GK") and 1 or 99 end
            local isAcademy = (rawYouth[pId] ~= nil or tonumber(val(p, "isacademy", 0)) == 1 or val(p, "isacademy", "false") == "true")
            
            local valM = math.floor(((ovr * ovr * 800) / 100000) * 10) / 100

            local natId = tonumber(val(p, "nationality", 0)) or tonumber(val(p, "nationid", 0)) or tonumber(val(p, "countryid", 0)) or 0
            local natName = get_nation_name(natId)

            table.insert(playersJson, string.format([[        {
            "id": "%d", "name": "%s", "displayName": "%s", "number": %d,
            "primaryPosition": "%s", "secondaryPosition": "%s", "tertiaryPosition": "%s",
            "age": %d, "birthDate": "%s", "overall": %d, "potential": %d,
            "wageK": 5, "valueM": %.2f, "headshotUrl": "", "isAcademy": %s,
            "nationality": "%s", "nationalityId": %d
        }]], pId, pName, pName, jerseyNum, posStr, secPosStr, tertPosStr, age, birthDateStr, ovr, pot, valM, isAcademy and "true" or "false", clean_str(natName), natId))

            table.insert(squadPlayersList, { id = tostring(pId), name = pName })

            -- Derive Current Season Transfers using strict July 1st boundaries
            if not isAcademy then
                local joinDays = tonumber(val(p, "playerjointeamdate", 0)) or 0
                if joinDays > 0 then
                    local joinDateStr, joinYear = decode_fifa_date(joinDays, currentActiveYear)
                    local joinMonth = tonumber(string.sub(joinDateStr, 6, 7)) or 1
                    
                    -- Season mathematics: If month is Jan-Jun (1-6), it belongs to the (Year-1) season.
                    local joinSeason = (joinMonth < 7) and (joinYear - 1) or joinYear
                    
                    if joinSeason == currentActiveYear then
                        -- Broad Regen Filter: If the player has a generated ID (>300,000) and is young (<=21),
                        -- the vast majority of the time this is a Youth Academy promotion, not an external purchase.
                        local isPromotion = false
                        if pId >= 300000 and age <= 21 then
                            isPromotion = true
                        end
                        
                        if isPromotion then
                            table.insert(currentSeasonSigningsJson, string.format([[        { "playerName": "%s", "type": "Promoted In", "feeM": 0.0, "fromToClub": "Youth Academy", "date": "%s" }]], pName, joinDateStr))
                        else
                            table.insert(currentSeasonSigningsJson, string.format([[        { "playerName": "%s", "type": "Transfer In", "feeM": %.2f, "fromToClub": "External Club", "date": "%s" }]], pName, valM, joinDateStr))
                        end
                    end
                end
            end
        end
    end

    -- Process youthplayers table directly for standalone rows (FC 24/25 fallback)
    for _, p in ipairs(safe_get_rows("youthplayers")) do
        local pId = tonumber(val(p, "playerid", 0)) or 0
        if pId > 0 and rawYouth[pId] ~= nil and rawSquad[pId] == nil then
            local pfname = val(p, "firstname", "")
            if pfname == "" then pfname = playernamesMap[tonumber(val(p, "firstnameid", 0)) or 0] or "" end
            local psname = val(p, "surname", "")
            if psname == "" then psname = val(p, "lastname", "") end
            if psname == "" then psname = playernamesMap[tonumber(val(p, "lastnameid", 0)) or 0] or "" end
            local rawFullName = ((pfname .. " " .. psname):gsub("^%s*(.-)%s*$", "%1"))
            if rawFullName == "" then rawFullName = psname ~= "" and psname or pfname end
            if rawFullName == "" then rawFullName = "Youth Player " .. pId end
            
            local pName = clean_str(rawFullName)
            local ovr = tonumber(val(p, "overallrating", 50)) or 50
            local pot = tonumber(val(p, "potential", 80)) or 80
            
            local birthDateStr, birthYear = decode_fifa_date(tonumber(val(p, "birthdate", 0)) or 0, currentActiveYear - 16)
            local age = currentActiveYear - birthYear
            if age < 15 or age > 21 then age = 16 end
            local posStr = playerPosMap[tonumber(val(p, "preferredposition1", 14)) or 14] or "CM"
            local jerseyNum = rawYouth[pId]
            if jerseyNum <= 0 then jerseyNum = (posStr == "GK") and 1 or 99 end

            table.insert(playersJson, string.format([[        {
            "id": "%d", "name": "%s", "displayName": "%s", "number": %d,
            "primaryPosition": "%s", "secondaryPosition": "", "tertiaryPosition": "",
            "age": %d, "birthDate": "%s", "overall": %d, "potential": %d,
            "wageK": 1, "valueM": 0.5, "headshotUrl": "", "isAcademy": true
        }]], pId, pName, pName, jerseyNum, posStr, age, birthDateStr, ovr, pot))

            table.insert(squadPlayersList, { id = tostring(pId), name = pName })
        end
    end

    local matchesJson = {}
    local oppList = leagueOpponentsMap[activeLeagueId] or { "Barrow", "AFC Wimbledon", "Notts County", "Salford City" }
    local winsRem, drawsRem, lossesRem = totalWins, totalDraws, totalLosses
    for i = 1, matchesPlayed do
        local oppName = oppList[((i - 1) % #oppList) + 1]
        local gf, ga, badge = 1, 0, "W"
        if winsRem > 0 and (i % 3 ~= 0 or (drawsRem == 0 and lossesRem == 0)) then
            gf = (i % 2 == 0) and 2 or 1; ga = (gf == 2) and 1 or 0; badge = "W"; winsRem = winsRem - 1
        elseif drawsRem > 0 and (i % 4 == 0 or winsRem == 0) then
            gf = (i % 2 == 0) and 1 or 0; ga = gf; badge = "D"; drawsRem = drawsRem - 1
        else
            gf = 0; ga = (i % 2 == 0) and 2 or 1; badge = "L"
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
            "id": "match-%d", "opponentName": "%s", "isHome": %s, "goalsFor": %d, "goalsAgainst": %d,
            "resultBadge": "%s", "matchDate": "%s", "competition": "%s", "leaguePosition": %d,
            "playerPerformances": [
%s
            ]
        }]], i, clean_str(oppName), (i % 2 == 1) and "true" or "false", gf, ga, badge, dateStr, leagueName, currentRank, table.concat(perfsJson, ",\n")))
    end

    local historyJson = {}
    local globalTransfersJson = {}

    for sIdx, mh in ipairs(allPastSeasons) do
        local seasonYear = rawStartYear + (sIdx - 1)
        
        local seasonTransfersJson = {}
        local bigBuy = clean_str(val(mh, "bigbuyplayername", ""))
        local bigBuyFee = tonumber(val(mh, "bigbuyamount", 0)) or 0
        if bigBuy ~= "" and bigBuyFee > 0 then
            local tRow = string.format([[                { "playerName": "%s", "type": "Transfer In", "feeM": %.2f, "fromToClub": "External Club", "date": "%d-08-01" }]], bigBuy, bigBuyFee / 1000000, seasonYear)
            table.insert(seasonTransfersJson, tRow)
        end
        local bigSell = clean_str(val(mh, "bigsellplayername", ""))
        local bigSellFee = tonumber(val(mh, "bigsellamount", 0)) or 0
        if bigSell ~= "" and bigSellFee > 0 then
            local tRow = string.format([[                { "playerName": "%s", "type": "Transfer Out", "feeM": %.2f, "fromToClub": "External Club", "date": "%d-08-15" }]], bigSell, bigSellFee / 1000000, seasonYear)
            table.insert(seasonTransfersJson, tRow)
        end

        table.insert(historyJson, string.format([[        {
            "year": %d, "leagueName": "%s", "finalPosition": %d, "matchesPlayed": %d,
            "points": %d, "wins": %d, "draws": %d, "losses": %d, "goalsFor": %d, "goalsAgainst": %d,
            "transfers": [
%s
            ]
        }]], seasonYear, get_league_name(tonumber(val(mh, "leagueid", 0)) or 0), tonumber(val(mh, "tableposition", 1)) or 1,
            tonumber(val(mh, "games_played", 0)) or 0, tonumber(val(mh, "points", 0)) or 0,
            tonumber(val(mh, "wins", 0)) or 0, tonumber(val(mh, "draws", 0)) or 0, tonumber(val(mh, "losses", 0)) or 0,
            tonumber(val(mh, "goals_for", 0)) or 0, tonumber(val(mh, "goals_against", 0)) or 0,
            table.concat(seasonTransfersJson, ",\n")))
    end

    -- Global Transfers block (Current active loans + newly inferred current season signings)
    for _, t in ipairs(currentSeasonSigningsJson) do table.insert(globalTransfersJson, t) end

    for _, loan in ipairs(safe_get_rows("playerloans")) do
        local fromTeamId = tonumber(val(loan, "teamidloanedfrom", 0)) or 0
        if fromTeamId > 0 then
            local pId = tonumber(val(loan, "playerid", 0)) or 0
            if rawSquad[pId] ~= nil and fromTeamId ~= userTeamId then
                local pName = get_player_name_from_id(pId)
                table.insert(globalTransfersJson, string.format([[        { "playerName": "%s", "type": "Loan In", "feeM": 0.0, "fromToClub": "%s", "date": "%d-07-15" }]], pName, clean_str(get_team_name(fromTeamId)), currentActiveYear))
            elseif fromTeamId == userTeamId then
                local pName = get_player_name_from_id(pId)
                table.insert(globalTransfersJson, string.format([[        { "playerName": "%s", "type": "Loan Out", "feeM": 0.0, "fromToClub": "External Club", "date": "%d-07-15" }]], pName, currentActiveYear))
            end
        end
    end

    local trophiesJson = {}
    for sIdx, mh in ipairs(allPastSeasons) do
        if (tonumber(val(mh, "tableposition", 0)) or 0) == 1 then
            table.insert(trophiesJson, string.format([[        { "name": "%s Champions (%d)", "iconUrl": "" }]], get_league_name(tonumber(val(mh, "leagueid", 0)) or 0), rawStartYear + (sIdx - 1)))
        end
    end

    local fullJson = string.format([[{
    "clubName": "%s", "managerName": "%s", "leagueName": "%s",
    "primaryColorHex": "%s", "secondaryColorHex": "%s", "transferBudget": %.1f, "startYear": %d,
    "seasonRecord": "%d-%d-%d", "isOnboarded": true, "activeInjuries": %d,
    "leagueTable": {
        "finalRank": "%d", "totalPoints": "%d", "wins": "%d", "draws": "%d", "losses": "%d",
        "goalsFor": "%d", "goalsAgainst": "%d", "goalDifference": "%s%d"
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
        clubName, managerName, leagueName, primaryHex, secondaryHex, transferBudgetM, rawStartYear,
        totalWins, totalDraws, totalLosses, activeInjuries,
        currentRank, totalPoints, totalWins, totalDraws, totalLosses, totalGF, totalGA,
        (totalGF - totalGA >= 0 and "+" or ""), (totalGF - totalGA),
        table.concat(playersJson, ",\n"), table.concat(matchesJson, ",\n"),
        table.concat(historyJson, ",\n"), table.concat(globalTransfersJson, ",\n"), table.concat(trophiesJson, ",\n")
    )

    local targetPath = "career_export.json"
    local userProfile = os.getenv("USERPROFILE")
    if userProfile and userProfile ~= "" then targetPath = userProfile .. "\\Desktop\\career_export.json" end

    local f = io.open(targetPath, "w")
    if f then f:write(fullJson); f:close(); my_log("SUCCESS: Exported to " .. targetPath) end
end

pcall(export_career_v35)
