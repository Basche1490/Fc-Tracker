import re
import os

def fix_screen(path):
    with open(path, "r") as f:
        content = f.read()

    # Revert the bad replacement
    content = content.replace("val displayPlayers = viewingSeason?.players ?: displayPlayers", "val displayPlayers = viewingSeason?.players ?: state.players")
    content = content.replace("val displayTransfers = viewingSeason?.transfers ?: displayTransfers", "val displayTransfers = viewingSeason?.transfers ?: state.transfers")
    
    # Hide FAB if archived (Transfers, Squad, Academy)
    content = content.replace("FloatingActionButton(\n            onClick = { showAddPlayerDialog = true }", "if (!isArchived) {\n        FloatingActionButton(\n            onClick = { showAddPlayerDialog = true }")
    content = content.replace("Icon(Icons.Default.Add, \"Add Player\", tint = MaterialTheme.colorScheme.onPrimary)\n        }", "Icon(Icons.Default.Add, \"Add Player\", tint = MaterialTheme.colorScheme.onPrimary)\n        }\n        }")

    content = content.replace("FloatingActionButton(\n            onClick = { showAddTransfer = true }", "if (!isArchived) {\n        FloatingActionButton(\n            onClick = { showAddTransfer = true }")
    content = content.replace("Icon(Icons.Default.Add, \"Log Transfer\", tint = MaterialTheme.colorScheme.onPrimary)\n        }", "Icon(Icons.Default.Add, \"Log Transfer\", tint = MaterialTheme.colorScheme.onPrimary)\n        }\n        }")
    
    with open(path, "w") as f:
        f.write(content)

fix_screen("app/src/main/java/com/example/ui/screens/SquadScreen.kt")
fix_screen("app/src/main/java/com/example/ui/screens/AcademyScreen.kt")
fix_screen("app/src/main/java/com/example/ui/screens/TransfersScreen.kt")
