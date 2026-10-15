import re

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "r") as f:
    content = f.read()

# 1. Update AcademyPlayerCard signature
content = content.replace(
    "fun AcademyPlayerCard(player: Player, onClick: (() -> Unit)? = null) {",
    "fun AcademyPlayerCard(player: Player, onClick: (() -> Unit)? = null, onPromote: (() -> Unit)? = null, onRelease: (() -> Unit)? = null) {"
)

# 2. Update Promote logic
content = content.replace(
    "onClick = { /* Promote logic */ },",
    "onClick = { onPromote?.invoke() },"
)

# 3. Update Release logic
content = content.replace(
    "onClick = { /* Release logic */ },",
    "onClick = { onRelease?.invoke() },"
)

# 4. Update the call in ProspectsTab
target_call = "AcademyPlayerCard(player, onClick = { playerToEdit = player })"
replacement_call = """AcademyPlayerCard(
                            player,
                            onClick = { playerToEdit = player },
                            onPromote = { viewModel.updatePlayer(player.copy(isAcademy = false)) },
                            onRelease = { viewModel.deletePlayer(player.id) }
                        )"""
content = content.replace(target_call, replacement_call)

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "w") as f:
    f.write(content)
