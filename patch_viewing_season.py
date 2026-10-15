import re
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

old_appstate = """    val leagueTable: LeagueTable = LeagueTable(),
    val historicalSeasons: List<HistoricalSeason> = emptyList()"""
new_appstate = """    val leagueTable: LeagueTable = LeagueTable(),
    val historicalSeasons: List<HistoricalSeason> = emptyList(),
    val viewingSeasonYear: Int? = null"""

if "val viewingSeasonYear: Int? = null" not in content:
    content = content.replace(old_appstate, new_appstate)

new_func = """
    fun setViewingSeasonYear(year: Int?) {
        _state.update { it.copy(viewingSeasonYear = year) }
    }
"""

if "fun setViewingSeasonYear" not in content:
    content = content.replace("fun endSeason() {", new_func + "\n    fun endSeason() {")

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
