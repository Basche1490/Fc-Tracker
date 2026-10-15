import re

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

# I need to calculate the initial starting overall for each player
prospects_logic = """                prospects.forEach { player ->
                    val earliestPlayer = state.historicalSeasons.sortedBy { it.year }.firstNotNullOfOrNull { s -> s.players.find { p -> p.id == player.id } }
                    val initialOvr = earliestPlayer?.startingOverall ?: player.startingOverall
                    val currentStartOvr = player.startingOverall
                    
                    Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                        Text(player.name, color = Color.White, fontSize = 12.sp, modifier = Modifier.weight(0.3f))
                        
                        Box(modifier = Modifier.weight(0.7f).height(16.dp)) {
                            // Max width is based on max potential or 100
                            val maxOvr = 100f
                            val startWidth = (initialOvr.toFloat() / maxOvr)
                            val currentWidth = (currentStartOvr.toFloat() / maxOvr)
                            
                            // Background bar (initial overall)
                            Box(modifier = Modifier.fillMaxWidth(startWidth).fillMaxHeight().background(Color.Gray.copy(alpha=0.5f), androidx.compose.foundation.shape.RoundedCornerShape(4.dp)))
                            
                            // Foreground bar (current starting overall growth)
                            if (currentWidth > startWidth) {
                                Box(modifier = Modifier.fillMaxWidth(currentWidth).fillMaxHeight().background(WinColor.copy(alpha=0.8f), androidx.compose.foundation.shape.RoundedCornerShape(4.dp)))
                            } else if (currentWidth < startWidth) {
                                Box(modifier = Modifier.fillMaxWidth(currentWidth).fillMaxHeight().background(LossColor.copy(alpha=0.8f), androidx.compose.foundation.shape.RoundedCornerShape(4.dp)))
                            } else {
                                Box(modifier = Modifier.fillMaxWidth(currentWidth).fillMaxHeight().background(DrawColor.copy(alpha=0.8f), androidx.compose.foundation.shape.RoundedCornerShape(4.dp)))
                            }
                        }
                        
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("${initialOvr} → ${currentStartOvr}", color = Color.White, fontSize = 12.sp, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                    }
                }"""

# Need to replace the inside of the Column
content = re.sub(r"prospects\.forEach \{ player ->.*?Text\(\"\$\{player\.startingOverall\} → \$\{player\.overall\}\".*?\}", prospects_logic, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)

