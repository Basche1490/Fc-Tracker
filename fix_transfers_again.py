import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

# I will find the bounds of DeployScoutModal
start = content.find("fun DeployScoutModal(")
end = content.find("@Composable\nfun ScoutNetworkModal")

if start != -1 and end != -1:
    old_modal = content[start:end]
    new_modal = """fun DeployScoutModal(allEafcPlayers: List<com.example.EafcPlayer>, onDismiss: () -> Unit, onSave: (com.example.ScoutReport) -> Unit) {
    var playerName by remember { mutableStateOf("") }
    var positionSelected by remember { mutableStateOf("ST") }
    var age by remember { mutableStateOf("") }
    var ratingRange by remember { mutableStateOf("") }
    var potentialRange by remember { mutableStateOf("") }
    var valueM by remember { mutableStateOf("") }
    var scoutName by remember { mutableStateOf("") }
    var recommendationSelected by remember { mutableStateOf("Sign") }

    Dialog(onDismissRequest = onDismiss) {
        Box(modifier = Modifier.fillMaxWidth().heightIn(max = 600.dp).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surface).padding(16.dp)) {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                item { Text("Create Scout Report", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White) }
                item {
                    var nameExpanded by remember { mutableStateOf(false) }
                    @OptIn(ExperimentalMaterial3Api::class)
                    ExposedDropdownMenuBox(expanded = nameExpanded, onExpandedChange = { nameExpanded = !nameExpanded }) {
                        OutlinedTextField(
                            value = playerName,
                            onValueChange = { 
                                playerName = it
                                nameExpanded = true
                            },
                            label = { Text("Player Name") },
                            modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(),
                            singleLine = true
                        )
                        if (playerName.isNotEmpty() && playerName.length >= 2) {
                            val filtered = allEafcPlayers.filter { it.team != "Retired" && (it.name.contains(playerName, ignoreCase = true) || it.commonName.contains(playerName, ignoreCase = true)) }.take(5)
                            if (filtered.isNotEmpty()) {
                                ExposedDropdownMenu(expanded = nameExpanded, onDismissRequest = { nameExpanded = false }) {
                                    filtered.forEach { p ->
                                        val displayName = if (p.commonName.isNotBlank()) "${p.commonName} (${p.name})" else p.name
                                        DropdownMenuItem(
                                            text = { Text(displayName) },
                                            onClick = {
                                                playerName = p.name
                                                nameExpanded = false
                                            }
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
                item {
                    var positionExpanded by remember { mutableStateOf(false) }
                    val positions = listOf("GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LM", "RM", "LW", "RW", "ST")
                    @OptIn(ExperimentalMaterial3Api::class)
                    ExposedDropdownMenuBox(expanded = positionExpanded, onExpandedChange = { positionExpanded = it }) {
                        OutlinedTextField(value = positionSelected, onValueChange = {}, readOnly = true, label = { Text("Position") }, modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(), trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = positionExpanded) })
                        ExposedDropdownMenu(expanded = positionExpanded, onDismissRequest = { positionExpanded = false }) {
                            positions.forEach { pos ->
                                DropdownMenuItem(text = { Text(pos) }, onClick = { positionSelected = pos; positionExpanded = false })
                            }
                        }
                    }
                }
                item { OutlinedTextField(value = age, onValueChange = { age = it }, label = { Text("Age") }, modifier = Modifier.fillMaxWidth()) }
                item { OutlinedTextField(value = ratingRange, onValueChange = { ratingRange = it }, label = { Text("Estimated Rating Range (78 - 82)") }, modifier = Modifier.fillMaxWidth()) }
                item { OutlinedTextField(value = potentialRange, onValueChange = { potentialRange = it }, label = { Text("Estimated Potential Range (86 - 91)") }, modifier = Modifier.fillMaxWidth()) }
                item { OutlinedTextField(value = valueM, onValueChange = { valueM = it }, label = { Text("Estimated Value (€M)") }, modifier = Modifier.fillMaxWidth()) }
                item { OutlinedTextField(value = scoutName, onValueChange = { scoutName = it }, label = { Text("Assigned Scout Name") }, modifier = Modifier.fillMaxWidth()) }
                item {
                    var recommendationExpanded by remember { mutableStateOf(false) }
                    val recommendations = listOf("Sign", "Keep Scouting", "Ignore")
                    @OptIn(ExperimentalMaterial3Api::class)
                    ExposedDropdownMenuBox(expanded = recommendationExpanded, onExpandedChange = { recommendationExpanded = it }) {
                        OutlinedTextField(value = recommendationSelected, onValueChange = {}, readOnly = true, label = { Text("Recommendation") }, modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(), trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = recommendationExpanded) })
                        ExposedDropdownMenu(expanded = recommendationExpanded, onDismissRequest = { recommendationExpanded = false }) {
                            recommendations.forEach { rec ->
                                DropdownMenuItem(text = { Text(rec) }, onClick = { recommendationSelected = rec; recommendationExpanded = false })
                            }
                        }
                    }
                }
                item {
                    Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth().padding(top = 16.dp)) {
                        TextButton(onClick = onDismiss) { Text("Cancel", color = Color.White) }
                        Button(onClick = {
                            val report = com.example.ScoutReport(
                                playerName = playerName,
                                position = positionSelected,
                                age = age,
                                ratingRange = ratingRange,
                                potentialRange = potentialRange,
                                value = valueM,
                                scoutName = scoutName,
                                recommendation = recommendationSelected
                            )
                            onSave(report)
                        }) { Text("Save Report") }
                    }
                }
            }
        }
    }
}
"""
    content = content[:start] + new_modal + content[end:]
    
    with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
        f.write(content)
