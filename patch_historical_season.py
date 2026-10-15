import re
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

historical_data_class = """data class HistoricalSeason(
    val id: String = java.util.UUID.randomUUID().toString(),
    val year: Int,
    val leagueName: String,
    val finalPosition: Int,
    val matches: List<MatchResult>,
    val players: List<Player>,
    val transfers: List<TransferLog>
)
"""

if "data class HistoricalSeason" not in content:
    content = content.replace("data class LeagueTable(", historical_data_class + "\ndata class LeagueTable(")

old_appstate = """    val leagueTable: LeagueTable = LeagueTable()"""
new_appstate = """    val leagueTable: LeagueTable = LeagueTable(),
    val historicalSeasons: List<HistoricalSeason> = emptyList()"""

if "val historicalSeasons: List<HistoricalSeason>" not in content:
    content = content.replace(old_appstate, new_appstate)

end_season_func = """
    fun endSeason() {
        _state.update { state ->
            val finalPosition = state.recentMatches.filter { it.competition == state.leagueName }.maxByOrNull { it.matchDate }?.leaguePosition ?: 1
            val completedSeason = HistoricalSeason(
                year = state.startYear,
                leagueName = state.leagueName,
                finalPosition = finalPosition,
                matches = state.recentMatches,
                players = state.players,
                transfers = state.transfers
            )
            
            // Reset for new season
            val resetPlayers = state.players.map { 
                it.copy(matchesPlayed = 0, goals = 0, assists = 0) 
            }
            
            state.copy(
                historicalSeasons = state.historicalSeasons + completedSeason,
                recentMatches = emptyList(),
                transfers = emptyList(),
                players = resetPlayers,
                startYear = state.startYear + 1
            )
        }
    }
"""

if "fun endSeason()" not in content:
    content = content.replace("    fun addMatchResult(", end_season_func + "\n    fun addMatchResult(")

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
