import re

with open("app/applet/telemetry_sync.lua", "r") as f:
    code = f.read()

# Replace rating mock
code = re.sub(
    r'-- Rating delta calculation is tricky.*?local matchRating = 6\.0 \+ \(goalsDiff \* 1\.5\) \+ \(assistsDiff \* 0\.8\)\s+if matchRating > 10\.0 then matchRating = 10\.0 end\s+if matchRating == 6\.0 and appsDiff > 0 then matchRating = 6\.5 end\s+-- Add performance block\s+local perfBlock = string\.format\(\'\{"playerName":"%s", "goals":%d, "assists":%d, "rating":%\.1f, "isSub":%s\}\',\s+pName, goalsDiff, assistsDiff, matchRating, "false"\)',
    r'''-- Add performance block (leaving out rating and sub timestamp to allow manual entry)
                        local perfBlock = string.format('{"playerName":"%s", "goals":%d, "assists":%d}',
                            pName, goalsDiff, assistsDiff)''',
    code, flags=re.DOTALL
)

# Replace simMinute for user goals
code = re.sub(
    r'-- Add goal details \(simulated minutes, as SQLite drops exact timestamps\)\s+for g = 1, goalsDiff do\s+local simMinute = math\.random\(12, 89\)\s+local goalBlock = string\.format\(\'\{"playerName":"%s", "minute":%d, "isOpponent":false\}\', pName, simMinute\)\s+if addedGoals then matchGoalsStr = matchGoalsStr \.\. "," else addedGoals = true end\s+matchGoalsStr = matchGoalsStr \.\. goalBlock\s+end',
    r'''-- Add goal details (no exact timestamps)
                        for g = 1, goalsDiff do
                            local goalBlock = string.format('{"playerName":"%s", "isOpponent":false}', pName)
                            if addedGoals then matchGoalsStr = matchGoalsStr .. "," else addedGoals = true end
                            matchGoalsStr = matchGoalsStr .. goalBlock
                        end''',
    code, flags=re.DOTALL
)

# Replace simMinute for opponent goals
code = re.sub(
    r'-- Add opponent goals\s+for g = 1, ga do\s+local simMinute = math\.random\(5, 90\)\s+local goalBlock = string\.format\(\'\{"playerName":"%s \(Opponent\)", "minute":%d, "isOpponent":true\}\', oppName, simMinute\)\s+if string\.len\(matchGoalsStr\) > 0 then matchGoalsStr = matchGoalsStr \.\. "," end\s+matchGoalsStr = matchGoalsStr \.\. goalBlock\s+end',
    r'''-- Add opponent goals (no exact timestamps)
                for g = 1, ga do
                    local goalBlock = string.format('{"playerName":"%s (Opponent)", "isOpponent":true}', oppName)
                    if string.len(matchGoalsStr) > 0 then matchGoalsStr = matchGoalsStr .. "," end
                    matchGoalsStr = matchGoalsStr .. goalBlock
                end''',
    code, flags=re.DOTALL
)

with open("app/applet/telemetry_sync.lua", "w") as f:
    f.write(code)

print("Patched!")
