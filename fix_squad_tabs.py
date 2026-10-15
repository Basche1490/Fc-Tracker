import re

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

content = content.replace("val activeSquad = state.players.filter", "val activeSquad = displayPlayers.filter")
content = content.replace("val rosterSquad = state.players.filter", "val rosterSquad = displayPlayers.filter")

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)
