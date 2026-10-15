import re

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

old_banner = """fun HeroBanner(state: AppState, onMenuClick: () -> Unit, onSeasonSelected: (Int?) -> Unit) {
    var seasonExpanded by remember { mutableStateOf(false) }"""

new_banner = """fun HeroBanner(state: AppState, onMenuClick: () -> Unit, onSeasonSelected: (Int?) -> Unit) {
    var seasonExpanded by remember { mutableStateOf(false) }
    var showNewSeasonDialog by remember { mutableStateOf(false) }
    
    if (showNewSeasonDialog) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { showNewSeasonDialog = false },
            title = { Text("Start New Season?") },
            text = { Text("This will archive the current season and begin a fresh one. Ensure you have played all matches before proceeding. Are you sure?") },
            confirmButton = {
                Button(onClick = {
                    showNewSeasonDialog = false
                    onSeasonSelected(-1)
                }) {
                    Text("Yes, Start New Season")
                }
            },
            dismissButton = {
                androidx.compose.material3.TextButton(onClick = { showNewSeasonDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }"""

content = content.replace(old_banner, new_banner)

old_nav = """                        DropdownMenuItem(
                            text = { Text("Start New Season") },
                            onClick = {
                                onSeasonSelected(-1) // Signals Start New Season
                                seasonExpanded = false
                            }
                        )"""

new_nav = """                        DropdownMenuItem(
                            text = { Text("Start New Season") },
                            onClick = {
                                showNewSeasonDialog = true
                                seasonExpanded = false
                            }
                        )"""

content = content.replace(old_nav, new_nav)

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)

