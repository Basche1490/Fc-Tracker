import re
with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_editor_start = r"fun PlayerPerformanceEditor\(\s*perf: PlayerPerformance,\s*roster: List<com\.example\.Player>,\s*onUpdate: \(PlayerPerformance\) -> Unit,\s*onSubstitute: \(teammateId: String, minute: Int, isOut: Boolean\) -> Unit\s*\) \{"
old_editor_end = r"                \}\n            \}\n            Spacer\(Modifier.height\(8.dp\)\)\n        \}\n    \}\n\}"

match = re.search(old_editor_start + r".*?" + old_editor_end, content, flags=re.DOTALL)
if match:
    old_editor_full = match.group(0)
    print("Found match!")
else:
    print("Could not find match.")

new_editor = """fun PlayerPerformanceEditor(
    perf: PlayerPerformance, 
    roster: List<com.example.Player>, 
    onUpdate: (PlayerPerformance) -> Unit,
    onSubstitute: (teammateId: String, minute: Int, isOut: Boolean) -> Unit
) {
    val player = roster.find { it.id == perf.playerId }
    val positions = listOfNotNull(player?.primaryPosition, player?.secondaryPosition, player?.tertiaryPosition).map { it.uppercase() }
    val isGk = positions.contains("GK")
    val isDef = positions.any { it in listOf("CB", "LB", "RB", "LWB", "RWB", "CDM") }
    val isMidFwd = positions.any { it in listOf("CM", "CAM", "LM", "RM", "LW", "RW", "ST", "CF") } || positions.isEmpty()

    Column(modifier = Modifier.fillMaxWidth().padding(top = 16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Rating: ${String.format("%.1f", perf.rating)}", color = Color.White, modifier = Modifier.width(100.dp))
            Slider(
                value = perf.rating.toFloat(),
                onValueChange = { onUpdate(perf.copy(rating = (it * 10).toInt() / 10.0)) },
                valueRange = 1f..10f,
                modifier = Modifier.weight(1f)
            )
        }
        
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedTextField(
                value = perf.goals.toString(), 
                onValueChange = { 
                    val newGoals = it.toIntOrNull() ?: 0
                    val newAssisters = perf.goalAssisters.toMutableList()
                    while(newAssisters.size < newGoals) newAssisters.add(null)
                    while(newAssisters.size > newGoals) newAssisters.removeLast()
                    onUpdate(perf.copy(goals = newGoals, goalAssisters = newAssisters))
                },
                label = { Text("Goals") },
                modifier = Modifier.weight(1f),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
            OutlinedTextField(
                value = perf.assists.toString(),
                onValueChange = { onUpdate(perf.copy(assists = it.toIntOrNull() ?: 0)) },
                label = { Text("Assists") },
                modifier = Modifier.weight(1f),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
        }
        
        if (perf.goals > 0) {
            perf.goalAssisters.forEachIndexed { index, assisterId ->
                var expanded by remember { mutableStateOf(false) }
                ExposedDropdownMenuBox(
                    expanded = expanded,
                    onExpandedChange = { expanded = it }
                ) {
                    val assisterName = roster.find { it.id == assisterId }?.displayName ?: "Unassisted"
                    OutlinedTextField(
                        value = assisterName,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Goal ${index + 1} Assisted By") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                        modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth()
                    )
                    ExposedDropdownMenu(
                        expanded = expanded,
                        onDismissRequest = { expanded = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Unassisted") },
                            onClick = { 
                                val newAssisters = perf.goalAssisters.toMutableList()
                                newAssisters[index] = null
                                onUpdate(perf.copy(goalAssisters = newAssisters))
                                expanded = false 
                            }
                        )
                        roster.forEach { teammate ->
                            if (teammate.id != perf.playerId) {
                                DropdownMenuItem(
                                    text = { Text(teammate.displayName) },
                                    onClick = { 
                                        val newAssisters = perf.goalAssisters.toMutableList()
                                        newAssisters[index] = teammate.id
                                        onUpdate(perf.copy(goalAssisters = newAssisters))
                                        expanded = false 
                                    }
                                )
                            }
                        }
                    }
                }
            }
        }
        
        // Passing & Shooting
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedTextField(
                value = perf.passAccuracy.toString(),
                onValueChange = { onUpdate(perf.copy(passAccuracy = it.toIntOrNull() ?: 0)) },
                label = { Text("Pass Acc. (%)") },
                modifier = Modifier.weight(1f),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
            if (!isGk) {
                OutlinedTextField(
                    value = perf.shotAccuracy.toString(),
                    onValueChange = { onUpdate(perf.copy(shotAccuracy = it.toIntOrNull() ?: 0)) },
                    label = { Text("Shot Acc. (%)") },
                    modifier = Modifier.weight(1f),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
            }
        }

        // Defensive Stats
        if (isDef || isMidFwd) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = perf.tackles.toString(),
                    onValueChange = { onUpdate(perf.copy(tackles = it.toIntOrNull() ?: 0)) },
                    label = { Text("Tackles") },
                    modifier = Modifier.weight(1f),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
                OutlinedTextField(
                    value = perf.interceptions.toString(),
                    onValueChange = { onUpdate(perf.copy(interceptions = it.toIntOrNull() ?: 0)) },
                    label = { Text("Interceptions") },
                    modifier = Modifier.weight(1f),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
            }
        }

        // Goalie Stats
        if (isGk) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = perf.saves.toString(),
                    onValueChange = { onUpdate(perf.copy(saves = it.toIntOrNull() ?: 0)) },
                    label = { Text("Saves") },
                    modifier = Modifier.weight(1f),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
            }
        }
        
        Row(horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = perf.yellowCard, onCheckedChange = { onUpdate(perf.copy(yellowCard = it)) })
                Text("Yellow", fontSize = 12.sp, color = Color.White)
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = perf.redCard, onCheckedChange = { onUpdate(perf.copy(redCard = it)) })
                Text("Red", fontSize = 12.sp, color = Color.White)
            }
            if (isGk || isDef) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = perf.cleanSheet, onCheckedChange = { onUpdate(perf.copy(cleanSheet = it)) })
                    Text("Clean Sheet", fontSize = 12.sp, color = Color.White)
                }
            }
        }
        
        var isSubbed by remember { mutableStateOf(perf.subInMinute != null || perf.subOutMinute != null) }
        var subIsOut by remember { mutableStateOf(perf.subOutMinute != null) }
        var subMinute by remember { mutableStateOf((perf.subOutMinute ?: perf.subInMinute)?.toString() ?: "") }
        
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = isSubbed, onCheckedChange = { isSubbed = it })
            Text("Involved in Substitution?", fontSize = 14.sp, color = Color.White)
        }
        
        if (isSubbed) {
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    RadioButton(selected = subIsOut, onClick = { subIsOut = true })
                    Text("Subbed Out", fontSize = 14.sp, color = Color.White)
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    RadioButton(selected = !subIsOut, onClick = { subIsOut = false })
                    Text("Subbed In", fontSize = 14.sp, color = Color.White)
                }
            }
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = subMinute,
                    onValueChange = { subMinute = it },
                    label = { Text("Minute") },
                    modifier = Modifier.weight(1f),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
                
                var teammateExpanded by remember { mutableStateOf(false) }
                var selectedTeammateName by remember { mutableStateOf("Select Teammate") }
                ExposedDropdownMenuBox(
                    expanded = teammateExpanded,
                    onExpandedChange = { teammateExpanded = it },
                    modifier = Modifier.weight(1f)
                ) {
                    OutlinedTextField(
                        value = selectedTeammateName,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text(if (subIsOut) "Replaced By" else "Replaced") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = teammateExpanded) },
                        modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth()
                    )
                    ExposedDropdownMenu(
                        expanded = teammateExpanded,
                        onDismissRequest = { teammateExpanded = false }
                    ) {
                        roster.forEach { teammate ->
                            if (teammate.id != perf.playerId) {
                                DropdownMenuItem(
                                    text = { Text(teammate.displayName) },
                                    onClick = { 
                                        val min = subMinute.toIntOrNull() ?: 0
                                        onSubstitute(teammate.id, min, subIsOut)
                                        selectedTeammateName = teammate.displayName
                                        teammateExpanded = false 
                                    }
                                )
                            }
                        }
                    }
                }
            }
            Spacer(Modifier.height(8.dp))
        }
    }
}"""

if match:
    content = content.replace(old_editor_full, new_editor)
    with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
        f.write(content)

