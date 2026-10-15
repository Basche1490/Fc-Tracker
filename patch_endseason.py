import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

# Update age in resetPlayers mapping
old_reset = """            val resetPlayers = state.players.map { 
                it.copy(matchesPlayed = 0, goals = 0, assists = 0) 
            }"""

new_reset = """            val resetPlayers = state.players.map { 
                val birthYear = try { it.birthDate?.split("-")?.get(0)?.toInt() ?: 2000 } catch(e: Exception) { 2000 }
                val newAge = (state.startYear + 1) - birthYear
                it.copy(matchesPlayed = 0, goals = 0, assists = 0, age = newAge) 
            }"""

content = content.replace(old_reset, new_reset)
# Wait, player class does not have birthDate in it?! Let me check `Player` data class again.
with open("patch_endseason_temp", "w") as f:
    f.write(content)
