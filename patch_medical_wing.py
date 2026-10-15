import re

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

# 1. Add matches to MedicalWingTab invocation
old_call = r"3 -> MedicalWingTab\(activeSquad, Modifier\.weight\(1f\), onPlayerUpdate = \{ viewModel\.updatePlayer\(it\) \}, onNavigateToFormation = \{ selectedTabIndex = 1 \}\)"
new_call = "3 -> MedicalWingTab(activeSquad, state.recentMatches, Modifier.weight(1f), onPlayerUpdate = { viewModel.updatePlayer(it) }, onNavigateToFormation = { selectedTabIndex = 1 })"
content = re.sub(old_call, new_call, content)

# 2. Rewrite MedicalWingTab to include active injuries list
old_medical = r"@OptIn\(androidx\.compose\.material3\.ExperimentalMaterial3Api::class\)\n@Composable\nfun MedicalWingTab\([\s\S]*?(?=@Composable\nfun PlayerRowDark)"

new_medical = """@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun MedicalWingTab(
    players: List<Player>, 
    recentMatches: List<com.example.MatchResult>,
    modifier: Modifier = Modifier,
    onPlayerUpdate: (Player) -> Unit = {},
    onNavigateToFormation: () -> Unit = {}
) {
    var expanded by remember { mutableStateOf(false) }
    var selectedPlayer by remember { mutableStateOf<Player?>(null) }
    var injuryName by remember { mutableStateOf("") }
    
    // Date Pickers state
    var showStartDatePicker by remember { mutableStateOf(false) }
    var showReturnDatePicker by remember { mutableStateOf(false) }
    var startDateMillis by remember { mutableStateOf<Long?>(null) }
    var returnDateMillis by remember { mutableStateOf<Long?>(null) }
    
    val datePickerStateStart = androidx.compose.material3.rememberDatePickerState()
    val datePickerStateReturn = androidx.compose.material3.rememberDatePickerState()
    
    val dateFormatter = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
    val startDateStr = startDateMillis?.let { dateFormatter.format(java.util.Date(it)) } ?: (selectedPlayer?.injuryStartDate ?: "")
    val returnDateStr = returnDateMillis?.let { dateFormatter.format(java.util.Date(it)) } ?: (selectedPlayer?.injuryReturnDate ?: "")

    var showFormationPopup by remember { mutableStateOf(false) }

    LazyColumn(modifier = modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text(if (selectedPlayer != null && selectedPlayer!!.isInjured) "Edit Injury" else "Add Injury", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(Modifier.height(16.dp))
                
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    androidx.compose.material3.ExposedDropdownMenuBox(
                        expanded = expanded,
                        onExpandedChange = { expanded = it }
                    ) {
                        OutlinedTextField(
                            value = selectedPlayer?.displayName ?: "",
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Select Player") },
                            modifier = Modifier.fillMaxWidth().menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true),
                            trailingIcon = { androidx.compose.material3.ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) }
                        )
                        ExposedDropdownMenu(
                            expanded = expanded,
                            onDismissRequest = { expanded = false }
                        ) {
                            players.filter { !it.isAcademy }.forEach { player ->
                                DropdownMenuItem(
                                    text = { Text(player.displayName) },
                                    onClick = {
                                        selectedPlayer = player
                                        injuryName = player.injuryName ?: ""
                                        startDateMillis = null
                                        returnDateMillis = null
                                        expanded = false
                                    }
                                )
                            }
                        }
                    }
                    OutlinedTextField(
                        value = injuryName,
                        onValueChange = { injuryName = it },
                        label = { Text("Injury Type (e.g. ACL Tear)") },
                        modifier = Modifier.fillMaxWidth()
                    )
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = startDateStr, 
                            onValueChange = {}, 
                            readOnly = true,
                            label = { Text("Start Date") }, 
                            modifier = Modifier.weight(1f),
                            trailingIcon = {
                                androidx.compose.material3.IconButton(onClick = { showStartDatePicker = true }) {
                                    Icon(Icons.Default.DateRange, "Select Start Date")
                                }
                            }
                        )
                        OutlinedTextField(
                            value = returnDateStr, 
                            onValueChange = {}, 
                            readOnly = true,
                            label = { Text("Return Date") }, 
                            modifier = Modifier.weight(1f),
                            trailingIcon = {
                                androidx.compose.material3.IconButton(onClick = { showReturnDatePicker = true }) {
                                    Icon(Icons.Default.DateRange, "Select Return Date")
                                }
                            }
                        )
                    }
                    
                    Spacer(Modifier.height(16.dp))
                    Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth()) {
                        if (selectedPlayer?.isInjured == true) {
                            TextButton(onClick = {
                                selectedPlayer?.let { p ->
                                    onPlayerUpdate(p.copy(isInjured = false, injuryName = null, injuryStartDate = null, injuryReturnDate = null))
                                    selectedPlayer = null
                                    injuryName = ""
                                    startDateMillis = null
                                    returnDateMillis = null
                                }
                            }) { Text("Clear / Delete Injury", color = Color.Red) }
                        }
                        Button(onClick = { 
                            selectedPlayer?.let { p ->
                                val isStarter = p.isStartingXI && !p.isInjured
                                val updatedPlayer = p.copy(
                                    isInjured = true,
                                    injuryName = injuryName,
                                    injuryStartDate = startDateStr.takeIf { it.isNotBlank() },
                                    injuryReturnDate = returnDateStr.takeIf { it.isNotBlank() },
                                    isStartingXI = false
                                )
                                onPlayerUpdate(updatedPlayer)
                                if (isStarter) {
                                    showFormationPopup = true
                                } else {
                                    selectedPlayer = null
                                    injuryName = ""
                                    startDateMillis = null
                                    returnDateMillis = null
                                }
                            }
                        }) {
                            Text("Save Injury Record")
                        }
                    }
                }
            }
        }
        
        item {
            Text("Active Injuries", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
        }
        
        val injuredPlayers = players.filter { it.isInjured }
        if (injuredPlayers.isEmpty()) {
            item {
                Text("No current injuries.", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        } else {
            items(injuredPlayers) { p ->
                val missedMatches = recentMatches.count { match -> 
                    val d1 = p.injuryStartDate
                    val d2 = p.injuryReturnDate
                    if (d1 != null && d2 != null) match.matchDate in d1..d2 else false
                }
                
                DarkCard(modifier = Modifier.fillMaxWidth().clickable { 
                    selectedPlayer = p
                    injuryName = p.injuryName ?: ""
                    startDateMillis = null
                    returnDateMillis = null
                }) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(MaterialTheme.colorScheme.surfaceVariant),
                            contentAlignment = Alignment.Center
                        ) {
                            if (p.headshotUrl.isNotEmpty()) {
                                coil.compose.SubcomposeAsyncImage(
                                    model = p.headshotUrl,
                                    contentDescription = "Player Headshot",
                                    modifier = Modifier.fillMaxSize(),
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    error = { Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.primary) }
                                )
                            } else {
                                Text(p.displayName.take(1), fontWeight = FontWeight.Bold)
                            }
                        }
                        Spacer(Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(p.displayName, fontWeight = FontWeight.Bold, color = Color.White, fontSize = 16.sp)
                            Text("${p.injuryName ?: "Unknown Injury"}", color = Color.Red, fontSize = 14.sp)
                            Text("Out: ${p.injuryStartDate ?: "?"} to ${p.injuryReturnDate ?: "?"}", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                        }
                        Column(horizontalAlignment = Alignment.End) {
                            Text("$missedMatches", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = MaterialTheme.colorScheme.primary)
                            Text("Matches Missed", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }

    if (showStartDatePicker) {
        androidx.compose.material3.DatePickerDialog(
            onDismissRequest = { showStartDatePicker = false },
            confirmButton = {
                androidx.compose.material3.TextButton(onClick = {
                    startDateMillis = datePickerStateStart.selectedDateMillis
                    showStartDatePicker = false
                }) { Text("OK") }
            }
        ) {
            androidx.compose.material3.DatePicker(state = datePickerStateStart)
        }
    }

    if (showReturnDatePicker) {
        androidx.compose.material3.DatePickerDialog(
            onDismissRequest = { showReturnDatePicker = false },
            confirmButton = {
                androidx.compose.material3.TextButton(onClick = {
                    returnDateMillis = datePickerStateReturn.selectedDateMillis
                    showReturnDatePicker = false
                }) { Text("OK") }
            }
        ) {
            androidx.compose.material3.DatePicker(state = datePickerStateReturn)
        }
    }

    if (showFormationPopup) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { 
                showFormationPopup = false 
                selectedPlayer = null
                injuryName = ""
            },
            title = { Text("Adjust Starting 11") },
            text = { Text("The injured player was in your Starting 11 and has been moved to the bench. Please adjust your formation.") },
            confirmButton = {
                Button(onClick = {
                    showFormationPopup = false
                    selectedPlayer = null
                    injuryName = ""
                    onNavigateToFormation()
                }) {
                    Text("Go to Formation")
                }
            },
            dismissButton = {
                androidx.compose.material3.TextButton(onClick = {
                    showFormationPopup = false
                    selectedPlayer = null
                    injuryName = ""
                }) {
                    Text("Dismiss")
                }
            }
        )
    }
}
"""

content = re.sub(old_medical, new_medical, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)
