import re

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "r") as f:
    content = f.read()

content = content.replace("DetailedPlayerStatsModal(player = it, showOvrGrowth = true", "DetailedPlayerStatsModal(state = state, player = it, showOvrGrowth = true")

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "w") as f:
    f.write(content)


with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "r") as f:
    content = f.read()

content = content.replace("DetailedPlayerStatsModal(player = it, onDismiss", "DetailedPlayerStatsModal(state = state, player = it, onDismiss")

with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "w") as f:
    f.write(content)
