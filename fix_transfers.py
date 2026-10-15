import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

# Update DeployScoutModal signature and implementation
old_modal_sig = "fun DeployScoutModal(allEafcPlayers: List<com.example.EafcPlayer>, onDismiss: () -> Unit)"
new_modal_sig = "fun DeployScoutModal(allEafcPlayers: List<com.example.EafcPlayer>, onDismiss: () -> Unit, onSave: (com.example.ScoutReport) -> Unit)"
content = content.replace(old_modal_sig, new_modal_sig)

# In TransfersScreen root, pass onSave to DeployScoutModal
content = content.replace(
"""        if (showDeployScoutModal) {
            DeployScoutModal(allEafcPlayers = emptyList()) { showDeployScoutModal = false }
        }""",
"""        if (showDeployScoutModal) {
            DeployScoutModal(
                allEafcPlayers = emptyList(),
                onDismiss = { showDeployScoutModal = false },
                onSave = { report -> 
                    viewModel.addScoutReport(report)
                    showDeployScoutModal = false 
                }
            )
        }""")

# Find and replace the DeployScoutModal items
content = re.sub(
r"item \{ OutlinedTextField\(value = \"\", onValueChange = \{\}, label = \{ Text\(\"Age\"\)",
r"var age by remember { mutableStateOf(\"\") }\n                var ratingRange by remember { mutableStateOf(\"\") }\n                var potentialRange by remember { mutableStateOf(\"\") }\n                var valueM by remember { mutableStateOf(\"\") }\n                var scoutName by remember { mutableStateOf(\"\") }\n                item { OutlinedTextField(value = age, onValueChange = { age = it }, label = { Text(\"Age\") }",
content
)

content = re.sub(r"item \{ OutlinedTextField\(value = \"\", onValueChange = \{\}, label = \{ Text\(\"Estimated Rating Range \(78 - 82\)\)\)", r"item { OutlinedTextField(value = ratingRange, onValueChange = { ratingRange = it }, label = { Text(\"Estimated Rating Range (78 - 82)\") }", content)
content = re.sub(r"item \{ OutlinedTextField\(value = \"\", onValueChange = \{\}, label = \{ Text\(\"Estimated Potential Range \(86 - 91\)\)\)", r"item { OutlinedTextField(value = potentialRange, onValueChange = { potentialRange = it }, label = { Text(\"Estimated Potential Range (86 - 91)\") }", content)
content = re.sub(r"item \{ OutlinedTextField\(value = \"\", onValueChange = \{\}, label = \{ Text\(\"Estimated Value \(€M\)\)\)", r"item { OutlinedTextField(value = valueM, onValueChange = { valueM = it }, label = { Text(\"Estimated Value (€M)\") }", content)
content = re.sub(r"item \{ OutlinedTextField\(value = \"\", onValueChange = \{\}, label = \{ Text\(\"Assigned Scout Name\"\)", r"item { OutlinedTextField(value = scoutName, onValueChange = { scoutName = it }, label = { Text(\"Assigned Scout Name\") }", content)

content = content.replace("Button(onClick = onDismiss) { Text(\"Save Report\") }", """Button(onClick = {
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
                        }) { Text("Save Report") }""")


# Update ScoutNetworkTab to display scout reports
old_scout_tab = """fun ScoutNetworkTab(state: AppState, onDeployScout: () -> Unit, onManageNetwork: () -> Unit) {
    Box(modifier = Modifier.fillMaxSize()) {
        Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Text("Active Scout Network", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Button(onClick = onManageNetwork, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.primary)) {
                    Text("Hire Scout", fontSize = 12.sp)
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(12.dp))
                    .background(MaterialTheme.colorScheme.surface)
                    .border(1.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(12.dp))
                    .padding(32.dp),
                contentAlignment = Alignment.Center
            ) {
                Text("No scouts hired.", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        
        FloatingActionButton(
            onClick = onDeployScout,
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp),
            containerColor = MaterialTheme.colorScheme.primary
        ) {
            Icon(Icons.Default.Add, contentDescription = "Deploy Scout", tint = MaterialTheme.colorScheme.onPrimary)
        }
    }
}"""

new_scout_tab = """fun ScoutNetworkTab(viewModel: com.example.MainViewModel, state: AppState, onDeployScout: () -> Unit, onManageNetwork: () -> Unit) {
    Box(modifier = Modifier.fillMaxSize()) {
        Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Text("Active Scout Network", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Button(onClick = onManageNetwork, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant, contentColor = MaterialTheme.colorScheme.primary)) {
                    Text("Hire Scout", fontSize = 12.sp)
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            
            if (state.scoutReports.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(MaterialTheme.colorScheme.surface)
                        .border(1.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(12.dp))
                        .padding(32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text("No scout reports.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            } else {
                androidx.compose.foundation.lazy.LazyColumn(
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    modifier = Modifier.weight(1f).fillMaxWidth()
                ) {
                    items(state.scoutReports, key = { it.id }) { report ->
                        DarkCard {
                            Column(modifier = Modifier.fillMaxWidth()) {
                                Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                                    Text(report.playerName, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                    Text(report.position, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                                }
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Age: ${report.age}", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                Text("Est. Rating: ${report.ratingRange} | Est. Potential: ${report.potentialRange}", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                Text("Value: ${state.currencySymbol}${report.value}M", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                Spacer(modifier = Modifier.height(8.dp))
                                Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                                    Text("Scout: ${report.scoutName}", fontSize = 12.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    Text("Rec: ${report.recommendation}", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = if (report.recommendation == "Sign") Color(0xFF4CAF50) else if (report.recommendation == "Ignore") MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary)
                                }
                                Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
                                    TextButton(onClick = { viewModel.removeScoutReport(report.id) }, contentPadding = PaddingValues(0.dp)) {
                                        Text("Delete", fontSize = 12.sp, color = MaterialTheme.colorScheme.error)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        FloatingActionButton(
            onClick = onDeployScout,
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .padding(16.dp),
            containerColor = MaterialTheme.colorScheme.primary
        ) {
            Icon(Icons.Default.Add, contentDescription = "Deploy Scout", tint = MaterialTheme.colorScheme.onPrimary)
        }
    }
}"""

content = content.replace(old_scout_tab, new_scout_tab)

# Update the call to ScoutNetworkTab to pass viewModel
content = content.replace("ScoutNetworkTab(state = state, onDeployScout =", "ScoutNetworkTab(viewModel = viewModel, state = state, onDeployScout =")

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(content)

print("Finished fixing TransfersScreen")
