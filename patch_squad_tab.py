import re
with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "r") as f:
    content = f.read()

definition = """    val viewingSeason = state.historicalSeasons.find { it.year == state.viewingSeasonYear }
    val displayMatches = viewingSeason?.matches ?: state.recentMatches
    val displayPlayers = viewingSeason?.players ?: state.players
"""

content = content.replace("fun SquadStatsAwardsTab(state: AppState, onPlayerClick: (com.example.Player) -> Unit = {}, onShowAwards: () -> Unit) {\n", "fun SquadStatsAwardsTab(state: AppState, onPlayerClick: (com.example.Player) -> Unit = {}, onShowAwards: () -> Unit) {\n" + definition)

# Also fix the previous sed where I just added displayMatches but not displayPlayers
content = content.replace("    val displayMatches = viewingSeason?.matches ?: state.recentMatches\n", "    val displayMatches = viewingSeason?.matches ?: state.recentMatches\n    val displayPlayers = viewingSeason?.players ?: state.players\n")

content = content.replace("state.players", "displayPlayers")
# Note: we need to revert `state.displayPlayers` if that happens, but it was just `state.players` before

with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "w") as f:
    f.write(content)
