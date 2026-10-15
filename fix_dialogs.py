import re

files = [
    "app/src/main/java/com/example/ui/screens/SquadScreen.kt",
    "app/src/main/java/com/example/ui/screens/AcademyScreen.kt",
    "app/src/main/java/com/example/ui/screens/TransfersScreen.kt"
]

for file in files:
    with open(file, "r") as f:
        content = f.read()

    # Revert all displayPlayers / displayTransfers replacements in the entire file EXCEPT for the main screen functions.
    # To do this safely, I will just re-read them from git and apply the targeted replacement correctly.
    pass

