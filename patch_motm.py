import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_motm = r"""                            if \(motmExpanded && motmSearchQuery\.isNotBlank\(\)\) \{
                                val topRealPlayers = listOf\(
.*?
                                \)
                                val allOptions = state\.players\.map \{ it\.displayName \} \+ topRealPlayers \+ listOf\("Opponent Player"\)
                                val filtered = allOptions\.filter \{ it\.contains\(motmSearchQuery, ignoreCase = true\) \}\.take\(5\)"""

new_motm = """                            if (motmExpanded && motmSearchQuery.isNotBlank()) {
                                val searchEafc = viewModel.searchPlayersAndTeams(motmSearchQuery).map { if (it.commonName.isNotBlank()) it.commonName else it.name }
                                val allOptions = state.players.map { it.displayName } + searchEafc + listOf("Opponent Player")
                                val filtered = allOptions.filter { it.contains(motmSearchQuery, ignoreCase = true) }.distinct().take(10)"""

content = re.sub(old_motm, new_motm, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
