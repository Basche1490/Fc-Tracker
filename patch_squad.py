import re

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

content = content.replace("EditPlayerDialog(player = it", "EditPlayerDialog(startYear = state.startYear, player = it")
content = content.replace("EditPlayerDialog(player = null", "EditPlayerDialog(startYear = state.startYear, player = null")

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)

