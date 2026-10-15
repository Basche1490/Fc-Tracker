import re

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "r") as f:
    content = f.read()

target = """                        AcademyPlayerCard(
                            player,
                            onClick = { playerToEdit = player },
                            onPromote = { viewModel.updatePlayer(player.copy(isAcademy = false)) },
                            onRelease = { viewModel.deletePlayer(player.id) }
                        )"""
replacement = """                        AcademyPlayerCard(
                            player,
                            onClick = { playerToEdit = player },
                            onPromote = { 
                                viewModel.updatePlayer(player.copy(isAcademy = false))
                                playerToEdit = null
                            },
                            onRelease = { 
                                viewModel.deletePlayer(player.id)
                                playerToEdit = null
                            }
                        )"""
content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "w") as f:
    f.write(content)
