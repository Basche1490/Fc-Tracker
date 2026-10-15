import re

with open("app/src/main/java/com/example/ui/screens/DetailedPlayerStatsModal.kt", "r") as f:
    content = f.read()

old_stats = """        val allPerformances: List<com.example.PlayerPerformance> = androidx.compose.runtime.remember(allMatches) {
            allMatches.mapNotNull { m -> (m.homePerformances + m.awayPerformances).find { p -> p.playerId == player.id } }
        }"""

new_stats = """        val allPerformances: List<com.example.PlayerPerformance> = androidx.compose.runtime.remember(allMatches) {
            allMatches.mapNotNull { m -> m.playerPerformances.find { p -> p.playerId == player.id } }
        }"""

content = content.replace(old_stats, new_stats)

with open("app/src/main/java/com/example/ui/screens/DetailedPlayerStatsModal.kt", "w") as f:
    f.write(content)

