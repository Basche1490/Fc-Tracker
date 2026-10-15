import re
with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

old_hero_sig = "fun HeroBanner(state: AppState, onMenuClick: () -> Unit) {"
new_hero_sig = "fun HeroBanner(state: AppState, onMenuClick: () -> Unit, onSeasonSelected: (Int?) -> Unit) {"
content = content.replace(old_hero_sig, new_hero_sig)

old_dropdown = """                Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .padding(horizontal = 12.dp, vertical = 6.dp)
                    ) {
                        Text("${state.startYear}/${state.startYear + 1}", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                    }"""

new_dropdown = """                Box {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(MaterialTheme.colorScheme.surfaceVariant)
                            .clickable { seasonExpanded = true }
                            .padding(horizontal = 12.dp, vertical = 6.dp)
                    ) {
                        val displayYear = state.viewingSeasonYear ?: state.startYear
                        val suffix = if (state.viewingSeasonYear == null) " (Current)" else " (Archived)"
                        Text("${displayYear}/${displayYear + 1}$suffix", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.width(4.dp))
                        Icon(androidx.compose.material.icons.Icons.Default.ArrowDropDown, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                    }
                    DropdownMenu(
                        expanded = seasonExpanded,
                        onDismissRequest = { seasonExpanded = false }
                    ) {
                        state.historicalSeasons.forEach { season ->
                            DropdownMenuItem(
                                text = { Text("${season.year}/${season.year + 1} (Archived)") },
                                onClick = {
                                    onSeasonSelected(season.year)
                                    seasonExpanded = false
                                }
                            )
                        }
                        DropdownMenuItem(
                            text = { Text("${state.startYear}/${state.startYear + 1} (Current)") },
                            onClick = {
                                onSeasonSelected(null)
                                seasonExpanded = false
                            }
                        )
                    }
                }"""

content = content.replace(old_dropdown, new_dropdown)

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)
