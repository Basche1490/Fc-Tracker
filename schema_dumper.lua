-- =========================================================================
-- EA SPORTS FC / FIFA CAREER MODE DB SCHEMA DUMPER
-- This script will dump all available tables, column names, and their 
-- data types into a text file on your Desktop.
-- =========================================================================

local function my_log(msg)
    local s = "[SchemaDumper] " .. tostring(msg)
    if type(log) == "function" then pcall(log, s) end
    if type(print) == "function" then pcall(print, s) end
end

local function dump_schema()
    my_log("Starting DB Schema Dump...")
    local userProfile = os.getenv("USERPROFILE") or ""
    local targetPath = "career_schema_dump.txt"
    if userProfile ~= "" then
        targetPath = userProfile .. "\\Desktop\\career_schema_dump.txt"
    end

    local f = io.open(targetPath, "w")
    if not f then
        my_log("ERROR: Could not open " .. targetPath .. " for writing.")
        return 
    end
    
    f:write("=================================================================\n")
    f:write(" EA SPORTS FC / FIFA CAREER MODE DB SCHEMA DUMP \n")
    f:write(" Generated on: " .. os.date("%Y-%m-%d %H:%M:%S") .. "\n")
    f:write("=================================================================\n\n")

    -- List of common tables to probe 
    -- (in case GetDBTableNames() is not available in the specific LE version)
    local tablesToProbe = {
        "players", "teams", "leagues", "leagueteamlinks", "teamplayerlinks", 
        "career_users", "career_managerhistory", "career_transferhistory", 
        "playerloans", "career_boardobjectives", "boardobjectives", 
        "youthplayers", "youthacademy", "editedteamnames", "createdteams",
        "manager", "managers", "stadiums", "teamstadiumlinks", "fixtures",
        "matchresults", "standings", "competitions", "playernames", 
        "career_calendar", "career_managerinfo", "career_playerinfo",
        "career_youthplayerinfo", "career_squadranking"
    }
    
    -- If the environment supports getting all table names dynamically, use it!
    if type(GetDBTableNames) == "function" then
        local ok, allTables = pcall(GetDBTableNames)
        if ok and type(allTables) == "table" and #allTables > 0 then
            tablesToProbe = allTables
            f:write("SUCCESS: Found GetDBTableNames API. Dumping " .. tostring(#tablesToProbe) .. " tables.\n\n")
        else
            f:write("NOTE: GetDBTableNames() returned empty. Using fallback table list.\n\n")
        end
    else
        f:write("NOTE: GetDBTableNames API not found. Using fallback table list.\n\n")
    end

    for _, tName in ipairs(tablesToProbe) do
        local ok, rows = pcall(GetDBTableRows, tName)
        if ok and type(rows) == "table" and #rows > 0 then
            f:write("TABLE: " .. tName .. "\n")
            f:write("TOTAL ROWS: " .. tostring(#rows) .. "\n")
            f:write("COLUMNS:\n")
            
            local firstRow = rows[1]
            local cols = {}
            for colName, _ in pairs(firstRow) do
                table.insert(cols, colName)
            end
            table.sort(cols)
            
            for _, colName in ipairs(cols) do
                local innerVal = firstRow[colName]
                local valType = type(innerVal)
                local sampleValue = tostring(innerVal)
                
                -- Live Editor rows often return objects with a `.value` property
                if type(innerVal) == "table" and innerVal.value ~= nil then
                    valType = type(innerVal.value)
                    sampleValue = tostring(innerVal.value)
                end
                
                -- Format the string nicely
                f:write(string.format("  - %-30s | Type: %-8s | Sample: %s\n", colName, valType, sampleValue))
            end
            f:write("\n-----------------------------------------------------------------\n\n")
        else
            f:write("TABLE: " .. tostring(tName) .. " (Empty or Not Found)\n")
            f:write("\n-----------------------------------------------------------------\n\n")
        end
    end
    
    f:close()
    my_log("SUCCESS: Schema successfully dumped to " .. targetPath)
end

-- Run safely
pcall(dump_schema)
