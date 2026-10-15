import os

with open("app/applet/career_exporter_v24.lua", "r") as f:
    content = f.read()

# 1. Add youthSquad Extraction
content = content.replace("""    local rawSquad = {}
    local activeInjuries = 0
    for _, tpl in ipairs(safe_get_rows("teamplayerlinks")) do""", """    local rawSquad = {}
    local rawYouth = {}
    local activeInjuries = 0
    
    -- Main Squad
    for _, tpl in ipairs(safe_get_rows("teamplayerlinks")) do""")

content = content.replace("""        end
    end

    local playerPosMap = {""", """        end
    end
    
    -- Youth Squad
    for _, yp in ipairs(safe_get_rows("youthplayers")) do
        if tonumber(val(yp, "teamid", 0)) == userTeamId then
            local pId = tonumber(val(yp, "playerid", 0)) or 0
            if pId > 0 then 
                rawYouth[pId] = tonumber(val(yp, "jerseynumber", 0)) or 0 
            end
        end
    end

    local playerPosMap = {""")

# 2. Merge tables for loop
content = content.replace("""    local playersJson = {}
    local squadPlayersList = {}
    local playerMap = {}

    for _, p in ipairs(safe_get_rows("players")) do""", """    local playersJson = {}
    local squadPlayersList = {}
    local playerMap = {}
    
    local allPlayersTable = safe_get_rows("players")
    for _, yp in ipairs(safe_get_rows("youthplayers")) do
        table.insert(allPlayersTable, yp)
    end

    for _, p in ipairs(allPlayersTable) do""")

# 3. Use rawYouth for isAcademy
content = content.replace("""            if rawSquad[pId] ~= nil then
                local ovr = tonumber(val(p, "overallrating", 70)) or 70""", """            if rawSquad[pId] ~= nil or rawYouth[pId] ~= nil then
                local ovr = tonumber(val(p, "overallrating", 70)) or 70""")

content = content.replace("""                local jerseyNum = rawSquad[pId]
                if jerseyNum <= 0 then jerseyNum = (posStr == "GK") and 1 or 99 end

                local isAcademy = (tonumber(val(p, "isacademy", 0)) == 1 or val(p, "isacademy", "false") == "true")""", """                local jerseyNum = rawSquad[pId] or rawYouth[pId]
                if jerseyNum <= 0 then jerseyNum = (posStr == "GK") and 1 or 99 end

                local isAcademy = (rawYouth[pId] ~= nil or tonumber(val(p, "isacademy", 0)) == 1 or val(p, "isacademy", "false") == "true")""")


content = content.replace("export_career_v24", "export_career_v25")
content = content.replace("(v24)", "(v25)")

with open("app/applet/career_exporter_v25.lua", "w") as f:
    f.write(content)
