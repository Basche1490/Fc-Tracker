local function my_log(msg)
    local s = "[TestDB] " .. tostring(msg)
    pcall(function()
        local userProfile = os.getenv("USERPROFILE")
        local logPath = "career_export_log.txt"
        if userProfile and userProfile ~= "" then
            logPath = userProfile .. "\\Desktop\\career_export_log.txt"
        end
        local f = io.open(logPath, "a")
        if f then f:write(os.date("%Y-%m-%d %H:%M:%S") .. " " .. s .. "\n"); f:close() end
    end)
end

local function safe_get_rows(tbl_name)
    local ok, res = pcall(GetDBTableRows, tbl_name)
    if ok and type(res) == "table" then return res end
    return {}
end

my_log("Testing youthplayers table:")
for i, row in ipairs(safe_get_rows("youthplayers")) do
    if i == 1 then
        for k, v in pairs(row) do my_log("youthplayers col: " .. k) end
    end
end
