import re

with open('app/src/main/java/com/example/ui/screens/MatchesScreen.kt', 'r') as f:
    text = f.read()

# Add states for the new grid
new_states = """    var xGAgainst by remember { mutableStateOf("0.0") }
    var leaguePosition by remember { mutableStateOf("1") }

    var playerPerformances by remember { mutableStateOf(state.players.take(11).map { PlayerPerformance(playerId = it.id) }) }
    var motmId by remember { mutableStateOf<String?>(null) }
"""
text = text.replace('    var xGAgainst by remember { mutableStateOf("0.0") }\n    var leaguePosition by remember { mutableStateOf("1") }', new_states)

# Add the UI for Lineup, MOTM, etc.
new_ui = """                item { OutlinedTextField(value = leaguePosition, onValueChange = { leaguePosition = it }, label = { Text("League Position") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.fillMaxWidth()) }

                item { Text("Lineup & Performances", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary) }
                
                item {
                    var expandedMotm by remember { mutableStateOf(false) }
                    ExposedDropdownMenuBox(expanded = expandedMotm, onExpandedChange = { expandedMotm = !expandedMotm }) {
                        OutlinedTextField(
                            value = state.players.find { it.id == motmId }?.name ?: "Select MOTM",
                            onValueChange = {}, readOnly = true, label = { Text("Man of the Match") },
                            modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth()
                        )
                        ExposedDropdownMenu(expanded = expandedMotm, onDismissRequest = { expandedMotm = false }) {
                            state.players.forEach { p ->
                                DropdownMenuItem(text = { Text(p.name) }, onClick = { motmId = p.id; expandedMotm = false })
                            }
                        }
                    }
                }
"""
text = text.replace('                item { OutlinedTextField(value = leaguePosition, onValueChange = { leaguePosition = it }, label = { Text("League Position") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.fillMaxWidth()) }', new_ui)

# Update the save button
save_match = """                            expectedGoals = xGFor.toDoubleOrNull() ?: 0.0,
                            expectedGoalsAgainst = xGAgainst.toDoubleOrNull() ?: 0.0,
                            leaguePosition = leaguePosition.toIntOrNull() ?: 1,
                            playerPerformances = playerPerformances.map { if (it.playerId == motmId) it.copy(isMotm = true) else it }
                        )"""
text = re.sub(r'                            expectedGoals = xGFor\.toDoubleOrNull\(\) \?: 0\.0,\n                            expectedGoalsAgainst = xGAgainst\.toDoubleOrNull\(\) \?: 0\.0,\n                            leaguePosition = leaguePosition\.toIntOrNull\(\) \?: 1\n                        \)', save_match, text)

with open('app/src/main/java/com/example/ui/screens/MatchesScreen.kt', 'w') as f:
    f.write(text)
