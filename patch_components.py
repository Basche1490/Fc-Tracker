import re
with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

def_str = """
    val viewingSeason = state.historicalSeasons.find { it.year == state.viewingSeasonYear }
    val displayMatches = viewingSeason?.matches ?: state.recentMatches
    val displayPlayers = viewingSeason?.players ?: state.players
"""

# Replace "fun FinancialOverviewCard(state: AppState) {" with the definition inside
content = content.replace("fun FinancialOverviewCard(state: AppState) {\n", "fun FinancialOverviewCard(state: AppState) {\n" + def_str)
content = content.replace("fun SquadSummaryStats(state: AppState) {\n", "fun SquadSummaryStats(state: AppState) {\n" + def_str)
content = content.replace("fun FormAndStanding(state: AppState, onNavigate: (String) -> Unit) {\n", "fun FormAndStanding(state: AppState, onNavigate: (String) -> Unit) {\n" + def_str)

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)
