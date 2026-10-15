# Let's write the complete Lua script to a test file and check its syntax with luac or python
lua_script = '''
local function safe_get_rows(tbl_name)
    local ok, res = pcall(GetDBTableRows, tbl_name)
    if ok and type(res) == "table" then
        return res
    end
    return {}
end

local function val(row, field, def)
    if row and row[field] and row[field].value ~= nil then
        return row[field].value
    end
    return def
end
'''
print("Checking structure...")
