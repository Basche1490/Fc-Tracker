import os

with open("app/applet/career_exporter_v23.lua", "r") as f:
    content = f.read()

# Fix Start Year again
content = content.replace("""    local rawStartYear = tonumber(val(u, "startyear", 2024)) or 2024
    local currentActiveYear = tonumber(val(u, "currentseason", rawStartYear)) or rawStartYear
    if currentActiveYear < 1900 then currentActiveYear = 2024 end
    
    -- Sync historical chronology: if we have past seasons, startYear might need to be anchored
    if rawStartYear > currentActiveYear then rawStartYear = currentActiveYear end""", """    -- Anchor perfectly to 2023 (EA FC 24 default) or whatever startyear is defined
    local rawStartYear = tonumber(val(u, "startyear", 2023)) or 2023
    -- Advance the active year strictly based on completed historical seasons
    local currentActiveYear = rawStartYear + #allPastSeasons""")

content = content.replace("export_career_v23", "export_career_v24")
content = content.replace("(v23)", "(v24)")

with open("app/applet/career_exporter_v24.lua", "w") as f:
    f.write(content)
