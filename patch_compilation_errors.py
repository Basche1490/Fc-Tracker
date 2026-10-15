import re

# Fix CareerSummaryScreen
with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "r") as f:
    content = f.read()

content = content.replace("displayStats.forEach { player ->", "allTimeStats.forEach { player ->")

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "w") as f:
    f.write(content)


# Fix DashboardScreen syntax error
with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

content = content.replace("""                    }
                }
                }
            }
        }
    }
}

@Composable
fun ObjectivesWidget""", """                    }
                }
            }
        }
    }
}

@Composable
fun ObjectivesWidget""")

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)


# Fix DetailedPlayerStatsModal type inferences
with open("app/src/main/java/com/example/ui/screens/DetailedPlayerStatsModal.kt", "r") as f:
    content = f.read()

old_stats = """        val allMatches = androidx.compose.runtime.remember(state.recentMatches, state.historicalSeasons) {
            (state.recentMatches + state.historicalSeasons.flatMap { it.matches }).sortedByDescending { it.matchDate }
        }
        val allPerformances = androidx.compose.runtime.remember(allMatches) {
            allMatches.mapNotNull { m -> (m.homePerformances + m.awayPerformances).find { it.playerId == player.id } }
        }"""

new_stats = """        val allMatches = androidx.compose.runtime.remember(state.recentMatches, state.historicalSeasons) {
            (state.recentMatches + state.historicalSeasons.flatMap { it.matches }).sortedByDescending { it.matchDate }
        }
        val allPerformances: List<com.example.PlayerPerformance> = androidx.compose.runtime.remember(allMatches) {
            allMatches.mapNotNull { m -> (m.homePerformances + m.awayPerformances).find { p -> p.playerId == player.id } }
        }"""

content = content.replace(old_stats, new_stats)

with open("app/src/main/java/com/example/ui/screens/DetailedPlayerStatsModal.kt", "w") as f:
    f.write(content)

