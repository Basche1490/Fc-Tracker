import re
with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

content = content.replace("fun RosterTab(players: List<Player>", "fun RosterTab(players: List<Player>, startYear: Int = 2025")
content = content.replace("0 -> RosterTab(rosterSquad", "0 -> RosterTab(rosterSquad, startYear = state.startYear")
content = content.replace("startYear = viewModel.state.value.startYear", "startYear = startYear")

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)

