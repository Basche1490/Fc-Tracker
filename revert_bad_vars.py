import re

files = [
    "app/src/main/java/com/example/ui/screens/SquadScreen.kt",
    "app/src/main/java/com/example/ui/screens/AcademyScreen.kt",
    "app/src/main/java/com/example/ui/screens/TransfersScreen.kt"
]

for file in files:
    with open(file, "r") as f:
        content = f.read()

    # Revert all global replacements
    content = content.replace("displayPlayers", "state.players")
    content = content.replace("displayTransfers", "state.transfers")
    
    # Fix the top-level declaration that got broken
    content = content.replace("val state.players = viewingSeason?.players ?: state.players", "val displayPlayers = viewingSeason?.players ?: state.players")
    content = content.replace("val state.transfers = viewingSeason?.transfers ?: state.transfers", "val displayTransfers = viewingSeason?.transfers ?: state.transfers")
    
    with open(file, "w") as f:
        f.write(content)
