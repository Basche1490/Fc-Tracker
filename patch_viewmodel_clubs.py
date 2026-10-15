import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

new_func = """    fun getUniqueClubs(): List<String> {
        loadAllEafcPlayers()
        return allEafcPlayers.map { it.team }.distinct().sorted()
    }
"""

content = content.replace("private fun loadAllEafcPlayers() {", new_func + "\n    private fun loadAllEafcPlayers() {")

# Also, update `teamSearchName` fallback in initializeGameData. If the user picks exactly from the dropdown, it matches exactly! So we should just remove the exact hardcoded matches or keep them as fallbacks, but ensure exact match works.
# Oh, exact match already works! `team.contains(teamSearchName, ignoreCase = true)`

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)

