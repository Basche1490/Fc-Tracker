import sys

with open("app/applet/career_exporter_v25.lua", "r") as f:
    content = f.read()

old_name_logic = """            local pfname = playernamesMap[tonumber(val(p, "firstnameid", 0)) or 0] or ""
            local psname = playernamesMap[tonumber(val(p, "lastnameid", 0)) or 0] or ""
            local pcname = playernamesMap[tonumber(val(p, "commonnameid", 0)) or 0] or ""
            local jnId = playernamesMap[tonumber(val(p, "playerjerseynameid", 0)) or 0] or ""
            
            local rawFullName = (pcname ~= "" and pcname) or ((pfname .. " " .. psname):gsub("^%s*(.-)%s*$", "%1"))
            if rawFullName == "" then rawFullName = jnId end
            if rawFullName == "" then rawFullName = "Player " .. pId end"""

new_name_logic = """            local pfname = val(p, "firstname", "")
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
            if rawFullName == "" then rawFullName = "Player " .. pId end"""

if old_name_logic in content:
    content = content.replace(old_name_logic, new_name_logic)
    with open("app/applet/career_exporter_v25.lua", "w") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Old logic not found!")
