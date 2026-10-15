local function fix_lua()
    local f = io.open("app/applet/career_exporter_v19.lua", "r")
    local lines = {}
    for line in f:lines() do
        table.insert(lines, line)
    end
    f:close()

    local out = io.open("app/applet/career_exporter_v19.lua", "w")
    local skip_history = false
    for _, line in ipairs(lines) do
        if line:find("local seasonYear = rawSeason > 1900 and rawSeason or %(rawStartYear %+ %(sIdx %- 1%)%)") then
            out:write("        local seasonYear = rawSeason > 1900 and rawSeason or (rawStartYear + (rawSeason - 1))\n")
        elseif line:find("table.insert%(historyJson, string.format%(%[%[        {") then
            out:write("        if finishPos > 0 then\n")
            out:write(line .. "\n")
        elseif line:find("%]%], seasonYear, hLeagueName, finishPos, pld, pts, hWins, hDraws, hLosses, hTotalGF, hTotalGA%)%)") then
            out:write(line .. "\n")
            out:write("        end\n")
        else
            out:write(line .. "\n")
        end
    end
    out:close()
end
fix_lua()
