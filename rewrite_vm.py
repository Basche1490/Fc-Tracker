import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

start = content.find("data class MatchResult(")
end = content.find("val resultBadge: String", start)
if end != -1:
    end = content.find("}", end) + 1 # End of resultBadge block
    end = content.find("}", end) + 1 # End of MatchResult class

new_match_result = """data class MatchResult(
    val id: String = UUID.randomUUID().toString(),
    val opponentName: String,
    val opponentCrestUrl: String = "",
    val isHome: Boolean,
    val goalsFor: Int,
    val goalsAgainst: Int,
    val matchDate: String,
    val competition: String,
    val stage: String = "",
    val isExtraTime: Boolean = false,
    val homePenalties: Int = 0,
    val awayPenalties: Int = 0,
    val possession: Int = 50,
    val passingAccuracy: Int = 80,
    val shotsFor: Int = 0,
    val shotsAgainst: Int = 0,
    val expectedGoals: Double = 0.0,
    val expectedGoalsAgainst: Double = 0.0,
    val leaguePosition: Int = 1,
    val motmName: String = "",
    val playerPerformances: List<PlayerPerformance> = emptyList(),
    val goalDetails: List<GoalDetail> = emptyList(),
    val substitutions: List<Substitution> = emptyList()
) {
    val resultBadge: String
        get() = when {
            goalsFor > goalsAgainst -> "W"
            goalsFor < goalsAgainst -> "L"
            else -> "D"
        }
}"""

content = content[:start] + new_match_result + content[end:]

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
