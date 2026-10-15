import re

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

prospects_widget = """
@Composable
fun TopProspectsWidget(state: AppState) {
    val viewingSeason = state.historicalSeasons.find { it.year == state.viewingSeasonYear }
    val displayPlayers = viewingSeason?.players ?: state.players
    
    val prospects = displayPlayers.filter { it.age <= 22 }.sortedByDescending { it.overall }.take(5)
    
    if (prospects.isNotEmpty()) {
        DarkCard(modifier = Modifier.fillMaxWidth()) {
            Text("Top Prospects (U22)", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
            Spacer(modifier = Modifier.height(16.dp))
            
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                prospects.forEach { player ->
                    Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                        Text(player.name, color = Color.White, fontSize = 12.sp, modifier = Modifier.weight(0.3f))
                        
                        Box(modifier = Modifier.weight(0.7f).height(16.dp)) {
                            // Max width is based on max potential or 100
                            val maxOvr = 100f
                            val startWidth = (player.startingOverall.toFloat() / maxOvr)
                            val currentWidth = (player.overall.toFloat() / maxOvr)
                            
                            // Background bar (start overall)
                            Box(modifier = Modifier.fillMaxWidth(startWidth).fillMaxHeight().background(Color.Gray.copy(alpha=0.5f), RoundedCornerShape(4.dp)))
                            
                            // Foreground bar (current overall growth)
                            if (currentWidth > startWidth) {
                                Box(modifier = Modifier.fillMaxWidth(currentWidth).fillMaxHeight().background(WinColor.copy(alpha=0.8f), RoundedCornerShape(4.dp)))
                            } else if (currentWidth < startWidth) {
                                Box(modifier = Modifier.fillMaxWidth(currentWidth).fillMaxHeight().background(LossColor.copy(alpha=0.8f), RoundedCornerShape(4.dp)))
                            } else {
                                Box(modifier = Modifier.fillMaxWidth(currentWidth).fillMaxHeight().background(DrawColor.copy(alpha=0.8f), RoundedCornerShape(4.dp)))
                            }
                        }
                        
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("${player.startingOverall} → ${player.overall}", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
    }
}
"""

if "fun TopProspectsWidget" not in content:
    content = content.replace("fun ObjectivesWidget(state: AppState) {", prospects_widget + "\n@Composable\nfun ObjectivesWidget(state: AppState) {")
    content = content.replace("item { ObjectivesWidget(state) }", "item { TopProspectsWidget(state) }\n                item { ObjectivesWidget(state) }")

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)

