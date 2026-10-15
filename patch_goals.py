import re
with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "r") as f:
    content = f.read()

old_goals = 'Text("Goals Conceded: ${goalsAgainst.toString().toInt()}", color = Color.White)'
new_goals = 'Text("Goals Conceded: $goalsAgainst", color = Color.White)'

content = content.replace(old_goals, new_goals)

with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "w") as f:
    f.write(content)
