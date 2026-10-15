import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

old_add = r"""    fun addMatchResult\(match: MatchResult\) \{
        _state\.update \{ it\.copy\(recentMatches = listOf\(match\) \+ it\.recentMatches\) \}
    \}"""

new_add = """    fun addMatchResult(match: MatchResult) {
        _state.update { state ->
            val updatedPlayers = state.players.map { player ->
                if (player.isInjured && player.injuryReturnDate != null && match.matchDate >= player.injuryReturnDate) {
                    player.copy(isInjured = false, injuryName = null, injuryStartDate = null, injuryReturnDate = null)
                } else {
                    player
                }
            }
            state.copy(
                recentMatches = listOf(match) + state.recentMatches,
                players = updatedPlayers
            )
        }
    }"""
content = re.sub(old_add, new_add, content)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
