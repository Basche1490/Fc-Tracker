import re

with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "r") as f:
    content = f.read()

# First, properly remove Hall of Fame
hof_pattern = r"        item \{\n            DarkCard\(modifier = Modifier\.fillMaxWidth\(\)\) \{\n                Text\(\"Season Hall of Fame.*?\}\n        \}"
content = re.sub(hof_pattern, "", content, flags=re.DOTALL)

# Add sorting click logic for the table headers and the "Avg" column
header_old = """                Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Player", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(2f))
                    Text("Apps", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                    Text("Gls", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                    Text("Asts", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                }"""

header_new = """                Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Player", fontWeight = FontWeight.Bold, color = if (sortMode == "Name") MaterialTheme.colorScheme.primary else Color.Gray, modifier = Modifier.weight(1.5f).clickable { sortMode = "Name" })
                    Text("Apps", fontWeight = FontWeight.Bold, color = if (sortMode == "Apps") MaterialTheme.colorScheme.primary else Color.Gray, modifier = Modifier.weight(1f).clickable { sortMode = "Apps" })
                    Text("Gls", fontWeight = FontWeight.Bold, color = if (sortMode == "Goals") MaterialTheme.colorScheme.primary else Color.Gray, modifier = Modifier.weight(1f).clickable { sortMode = "Goals" })
                    Text("Ast", fontWeight = FontWeight.Bold, color = if (sortMode == "Assists") MaterialTheme.colorScheme.primary else Color.Gray, modifier = Modifier.weight(1f).clickable { sortMode = "Assists" })
                    Text("Avg", fontWeight = FontWeight.Bold, color = if (sortMode == "Rating") MaterialTheme.colorScheme.primary else Color.Gray, modifier = Modifier.weight(1f).clickable { sortMode = "Rating" })
                }
                
                val sortedStats = when(sortMode) {
                    "Name" -> seasonStatsMap.sortedBy { it.player.displayName }
                    "Apps" -> seasonStatsMap.sortedByDescending { it.apps }
                    "Goals" -> seasonStatsMap.sortedByDescending { it.goals }
                    "Assists" -> seasonStatsMap.sortedByDescending { it.assists }
                    else -> seasonStatsMap.sortedByDescending { it.avgRating }
                }"""

content = content.replace(header_old, header_new)

# Now iterate over sortedStats instead of seasonStatsMap and render Avg
table_old = """                seasonStatsMap.forEach { stat ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { onPlayerClick(stat.player) }
                            .padding(vertical = 8.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("${stat.player.displayName}", color = Color.White, modifier = Modifier.weight(2f))
                        Text("${stat.apps}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text("${stat.goals}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text("${stat.assists}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                    }
                }"""

table_new = """                sortedStats.forEach { stat ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { onPlayerClick(stat.player) }
                            .padding(vertical = 8.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("${stat.player.displayName}", color = Color.White, modifier = Modifier.weight(1.5f), maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                        Text("${stat.apps}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text("${stat.goals}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text("${stat.assists}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text(String.format("%.1f", stat.avgRating), color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                    }
                }"""

content = content.replace(table_old, table_new)

with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "w") as f:
    f.write(content)

