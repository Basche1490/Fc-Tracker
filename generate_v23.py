import os

with open("app/applet/career_exporter_v22.lua", "r") as f:
    content = f.read()

# Fix Start Year
content = content.replace("""    local allPastSeasons = {}
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
    local currentActiveYear = currentSeasonStartYear""", """    local allPastSeasons = {}
    for _, mh in ipairs(safe_get_rows("career_managerhistory")) do
        local pos = tonumber(val(mh, "tableposition", 1)) or 1
        local tId = tonumber(val(mh, "teamid", 0)) or 0
        if tId == userTeamId and pos > 0 then
            table.insert(allPastSeasons, mh)
        end
    end
    table.sort(allPastSeasons, function(a, b) return (tonumber(val(a, "season", 0)) or 0) < (tonumber(val(b, "season", 0)) or 0) end)
    
    local rawStartYear = tonumber(val(u, "startyear", 2024)) or 2024
    local currentActiveYear = tonumber(val(u, "currentseason", rawStartYear)) or rawStartYear
    if currentActiveYear < 1900 then currentActiveYear = 2024 end
    
    -- Sync historical chronology: if we have past seasons, startYear might need to be anchored
    if rawStartYear > currentActiveYear then rawStartYear = currentActiveYear end""")

# Remove complex YA Team search
content = content.replace("""    -- 2. YOUTH ACADEMY IDENTIFICATION
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
    end""", """    -- 2. YOUTH ACADEMY IDENTIFICATION
    -- Removed separate academy team ID search. Academy players are linked to main team with `isacademy` flag.""")

# Fix Squad Extraction
content = content.replace("""    -- Squad Extraction
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
    end""", """    -- Squad Extraction
    local rawSquad = {}
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
        end
    end""")

# Fix isAcademy flag
content = content.replace("""            if rawSquad[pId] ~= nil or rawAcademy[pId] ~= nil then
                local ovr = tonumber(val(p, "overallrating", 70)) or 70""", """            if rawSquad[pId] ~= nil then
                local ovr = tonumber(val(p, "overallrating", 70)) or 70""")

content = content.replace("""                local jerseyNum = rawSquad[pId] or rawAcademy[pId]
                if jerseyNum <= 0 then jerseyNum = (posStr == "GK") and 1 or 99 end

                local isAcademy = (rawAcademy[pId] ~= nil)""", """                local jerseyNum = rawSquad[pId]
                if jerseyNum <= 0 then jerseyNum = (posStr == "GK") and 1 or 99 end

                local isAcademy = (tonumber(val(p, "isacademy", 0)) == 1 or val(p, "isacademy", "false") == "true")""")

content = content.replace("export_career_v22", "export_career_v23")
content = content.replace("(v22)", "(v23)")

with open("app/applet/career_exporter_v23.lua", "w") as f:
    f.write(content)
