import re

with open("app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt", "r") as f:
    content = f.read()

content = content.replace("overall = player?.overall ?: (startingOverall.toIntOrNull() ?: 60)", "overall = startingOverall.toIntOrNull() ?: 60")

with open("app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt", "w") as f:
    f.write(content)
