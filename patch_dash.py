import sys
with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

insert_widget = """
@Composable
fun LiveTelemetryWidget(state: AppState, viewModel: MainViewModel) {
    DarkCard(modifier = Modifier.fillMaxWidth()) {
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("Live Events Feed", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
            androidx.compose.material3.IconButton(onClick = { viewModel.fetchLiveTelemetry() }, modifier = Modifier.size(24.dp)) {
                androidx.compose.material3.Icon(androidx.compose.material.icons.Icons.Default.Refresh, contentDescription = "Refresh", tint = MaterialTheme.colorScheme.primary)
            }
        }
        Spacer(Modifier.height(12.dp))
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            if (state.liveEvents.isEmpty()) {
                Text("No live telemetry events yet. Play a match with the PC bridge running!", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
            } else {
                state.liveEvents.take(3).forEach { ev ->
                    Row(
                        modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(8.dp)).background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)).padding(12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        androidx.compose.material3.Icon(androidx.compose.material.icons.Icons.Default.Notifications, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(16.dp))
                        Spacer(Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(ev.title, fontSize = 12.sp, color = Color.White, fontWeight = FontWeight.Medium)
                            Text(ev.message, fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }
}
"""

content = content.replace("item { ObjectivesWidget(state, viewModel) }", "item { ObjectivesWidget(state, viewModel) }\n                item { LiveTelemetryWidget(state, viewModel) }")
content = content + "\n" + insert_widget

# Add a LaunchedEffect
content = content.replace("val displayPlayers = viewingSeason?.players?.takeIf { it.isNotEmpty() } ?: state.players", "val displayPlayers = viewingSeason?.players?.takeIf { it.isNotEmpty() } ?: state.players\n    androidx.compose.runtime.LaunchedEffect(Unit) {\n        viewModel.fetchLiveTelemetry()\n    }")

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)
