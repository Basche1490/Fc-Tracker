import sys

with open("app/applet/career_exporter_v21.lua", "r") as f:
    content = f.read()

content = content.replace('        if bigSell ~= "" and bigSellFee > 0 then\n            table.insert(historicalTransfersJson, string.format([[        { "playerName": "%s", "type": "Transfer Out", "feeM": %.2f, "fromToClub": "To External Club", "date": "%d-08-15" }]], bigSell, bigSellFee / 1000000, seasonYear))\n        end\n    end', '        if bigSell ~= "" and bigSellFee > 0 then\n            table.insert(historicalTransfersJson, string.format([[        { "playerName": "%s", "type": "Transfer Out", "feeM": %.2f, "fromToClub": "To External Club", "date": "%d-08-15" }]], bigSell, bigSellFee / 1000000, seasonYear))\n        end\n        ::skip_season::\n    end')

with open("app/applet/career_exporter_v21.lua", "w") as f:
    f.write(content)
