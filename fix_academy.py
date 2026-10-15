import re

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "EditYouthPlayerDialog(onDismiss = { showYouthForm = false }, onUpdate = { viewModel.addPlayer(it) })",
    "EditYouthPlayerDialog(startYear = state.startYear, onDismiss = { showYouthForm = false }, onUpdate = { viewModel.addPlayer(it) })"
)

content = content.replace(
    "EditYouthPlayerDialog(\n                player = playerToEdit,",
    "EditYouthPlayerDialog(\n                startYear = state.startYear,\n                player = playerToEdit,"
)

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "w") as f:
    f.write(content)
