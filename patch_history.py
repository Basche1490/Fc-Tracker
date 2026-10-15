import sys

with open("app/applet/career_exporter_v21.lua", "r") as f:
    lines = f.readlines()

out = []
for line in lines:
    out.append(line)
    if 'local finishPos = tonumber(val(mh, "tableposition", 1)) or 1' in line:
        out.append('        if finishPos == 0 then goto skip_season end\n')
    if 'end\n' == line and 'table.insert(historicalTransfersJson' in lines[lines.index(line)-2]:
        out.append('        ::skip_season::\n')

with open("app/applet/career_exporter_v21.lua", "w") as f:
    for line in out:
        f.write(line)
