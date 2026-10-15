import re

# Fix AcademyScreen.kt
with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "r") as f:
    content = f.read()

content = content.replace("viewModel.removePlayer(playerToEdit!!)", "viewModel.deletePlayer(playerToEdit!!.id)")
with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "w") as f:
    f.write(content)

# Fix TransfersScreen.kt ScoutNetworkTab and the invocation
with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

# Fix the invocation back to original if we change signature to not need viewModel, OR change the signature.
# Since we need to delete scout reports, we do need viewModel. Let's just fix the invocation and the signature.

start = content.find("fun ScoutNetworkTab(state: AppState, onDeployScout:")
end = content.find("fun TransferFormModal(", start)

if start != -1 and end != -1:
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
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Text("Scouted Prospects Board", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
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
                    Text("Awaiting scout reports...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            } else {
                LazyColumn(
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
}

@OptIn(ExperimentalMaterial3Api::class)
"""
    content = content[:start] + new_scout_tab + content[end:]

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(content)
