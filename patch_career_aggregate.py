import re
with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "r") as f:
    content = f.read()

aggregate_func = """@Composable
fun CareerSummaryScreen(viewModel: MainViewModel, onMenuClick: () -> Unit) {
    val state by viewModel.state.collectAsState()
    var showGraphicCard by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }

    // Calculate aggregated all-time stats
    val allTimeStats = remember(state.players, state.historicalSeasons) {
        val map = mutableMapOf<String, com.example.Player>()
        // Initialize with current stats
        state.players.forEach { p ->
            map[p.id] = p.copy() // Start with current baseline
        }
        
        // Add historical stats
        state.historicalSeasons.forEach { season ->
            season.players.forEach { hp ->
                val current = map[hp.id]
                if (current != null) {
                    map[hp.id] = current.copy(
                        matchesPlayed = current.matchesPlayed + hp.matchesPlayed,
                        goals = current.goals + hp.goals,
                        assists = current.assists + hp.assists,
                        // Note: A true avg rating would need weighted average, this is simplified for milestones
                    )
                } else {
                    map[hp.id] = hp
                }
            }
        }
        map.values.toList()
    }
"""

content = content.replace("@Composable\nfun CareerSummaryScreen(viewModel: MainViewModel, onMenuClick: () -> Unit) {\n    val state by viewModel.state.collectAsState()\n    var showGraphicCard by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }", aggregate_func)

# Now replace `state.players` with `allTimeStats` in the rest of CareerSummaryScreen
# Wait, only in the sections for players.
content = content.replace("val topPlayers = state.players.sortedByDescending", "val topPlayers = allTimeStats.sortedByDescending")
content = content.replace("val mostApps = state.players.maxByOrNull", "val mostApps = allTimeStats.maxByOrNull")
content = content.replace("val topScorer = state.players.maxByOrNull", "val topScorer = allTimeStats.maxByOrNull")
content = content.replace("val topAssists = state.players.maxByOrNull", "val topAssists = allTimeStats.maxByOrNull")
content = content.replace("val highestAvg = state.players.filter", "val highestAvg = allTimeStats.filter")
content = content.replace("state.players.forEach { player ->\n                            Row(", "allTimeStats.forEach { player ->\n                            Row(")

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "w") as f:
    f.write(content)
