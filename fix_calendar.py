import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

bad_block = """    val monthFmt = SimpleDateFormat("MMMM yyyy", Locale.getDefault())
        val displayMatches = if (state.viewingSeasonYear != null) {
        state.historicalSeasons.find { it.year == state.viewingSeasonYear }?.matches ?: emptyList()
    } else {
        state.recentMatches
    }
    val isArchived = state.viewingSeasonYear != null

    val df = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())"""

good_block = """    val monthFmt = SimpleDateFormat("MMMM yyyy", Locale.getDefault())
    val df = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())"""

content = content.replace(bad_block, good_block)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

