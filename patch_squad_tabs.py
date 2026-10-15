import re

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

old_active = r"val activeSquad = state\.players\.filter \{ it\.status != \"Sold\" && it\.status != \"Loaned Out\" \}\n            when \(selectedTabIndex\) \{"
new_active = """val activeSquad = state.players.filter { it.status != "Sold" && it.status != "Loaned Out" && !it.isLoanedOut }
            val rosterSquad = state.players.filter { it.status != "Sold" }
            when (selectedTabIndex) {"""
content = re.sub(old_active, new_active, content)

old_roster = r"0 -> RosterTab\(activeSquad, Modifier\.weight\(1f\)"
new_roster = r"0 -> RosterTab(rosterSquad, Modifier.weight(1f)"
content = re.sub(old_roster, new_roster, content)

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)
