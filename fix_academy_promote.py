import re

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "viewModel.updatePlayer(player.copy(isAcademy = false))",
    "viewModel.updatePlayer(player.copy(isAcademy = false, isPromoted = true))"
)

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "w") as f:
    f.write(content)

