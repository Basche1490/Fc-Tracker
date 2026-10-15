import re
with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "r") as f:
    content = f.read()

def_str = """
    val viewingSeason = state.historicalSeasons.find { it.year == state.viewingSeasonYear }
    val displayMatches = viewingSeason?.matches ?: state.recentMatches
    val displayPlayers = viewingSeason?.players ?: state.players
"""

content = content.replace("fun OverviewTab(state: AppState, viewModel: MainViewModel) {\n", "fun OverviewTab(state: AppState, viewModel: MainViewModel) {\n" + def_str)
content = content.replace("fun AwardsModal(state: AppState, viewModel: MainViewModel, onDismiss: () -> Unit) {\n", "fun AwardsModal(state: AppState, viewModel: MainViewModel, onDismiss: () -> Unit) {\n" + def_str)

with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "w") as f:
    f.write(content)
