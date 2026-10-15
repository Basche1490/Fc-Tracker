import re

with open('app/src/main/java/com/example/ui/screens/TransfersScreen.kt', 'r') as f:
    text = f.read()

# Update TransferFormModal
modal_replacement = """@Composable
fun TransferFormModal(viewModel: com.example.MainViewModel, onDismiss: () -> Unit) {
    Dialog(onDismissRequest = onDismiss) {
        Box(modifier = Modifier.fillMaxWidth().heightIn(max = 600.dp).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surface).padding(16.dp)) {
            LazyColumn(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                item { Text("Log Transfer Deal", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White) }
                item {
                    var typeExpanded by remember { mutableStateOf(false) }
                    var transferType by remember { mutableStateOf("In (Permanent)") }
                    val transferTypes = listOf("In (Permanent)", "Out (Permanent)", "In (Loan)", "Out (Loan)", "Free Agent Sign")
                    @OptIn(ExperimentalMaterial3Api::class)
                    ExposedDropdownMenuBox(expanded = typeExpanded, onExpandedChange = { typeExpanded = it }) {
                        OutlinedTextField(value = transferType, onValueChange = {}, readOnly = true, label = { Text("Transfer Type") }, modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(), trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = typeExpanded) })
                        ExposedDropdownMenu(expanded = typeExpanded, onDismissRequest = { typeExpanded = false }) {
                            transferTypes.forEach { type ->
                                DropdownMenuItem(text = { Text(type) }, onClick = { transferType = type; typeExpanded = false })
                            }
                        }
                    }
                }
                item {
                    var playerQuery by remember { mutableStateOf("") }
                    var searchResults by remember { mutableStateOf(emptyList<com.example.EafcPlayer>()) }
                    var searchExpanded by remember { mutableStateOf(false) }
                    
                    @OptIn(ExperimentalMaterial3Api::class)
                    ExposedDropdownMenuBox(
                        expanded = searchExpanded,
                        onExpandedChange = { searchExpanded = it }
                    ) {
                        OutlinedTextField(
                            value = playerQuery,
                            onValueChange = { 
                                playerQuery = it
                                searchResults = viewModel.searchPlayersAndTeams(it)
                                searchExpanded = searchResults.isNotEmpty()
                            },
                            label = { Text("Player Name") },
                            modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth()
                        )
                        ExposedDropdownMenu(
                            expanded = searchExpanded,
                            onDismissRequest = { searchExpanded = false }
                        ) {
                            searchResults.forEach { p ->
                                val dispName = if (p.commonName.isNotEmpty()) p.commonName else p.name
                                DropdownMenuItem(
                                    text = { Text("$dispName (${p.rating}) - ${p.team}") },
                                    onClick = {
                                        playerQuery = dispName
                                        searchExpanded = false
                                    }
                                )
                            }
                        }
                    }
                }
                
                var includeSwap by remember { mutableStateOf(false) }
                item { 
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = includeSwap, onCheckedChange = { includeSwap = it })
                        Text("Include Player Swap", color = Color.White)
                    }
                }
                var isRegen by remember { mutableStateOf(false) }
                item { 
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Checkbox(checked = isRegen, onCheckedChange = { isRegen = it })
                        Text("Is Regen", color = Color.White)
                    }
                }
                
                var teamQuery by remember { mutableStateOf("") }
                item {
                    var teamResults by remember { mutableStateOf(emptyList<String>()) }
                    var teamExpanded by remember { mutableStateOf(false) }
                    
                    @OptIn(ExperimentalMaterial3Api::class)
                    ExposedDropdownMenuBox(
                        expanded = teamExpanded,
                        onExpandedChange = { teamExpanded = it }
                    ) {
                        OutlinedTextField(
                            value = teamQuery,
                            onValueChange = { 
                                teamQuery = it
                                teamResults = viewModel.searchPlayersAndTeams(it).map { it.team }.distinct()
                                teamExpanded = teamResults.isNotEmpty()
                            },
                            label = { Text("Opponent Team Search") },
                            modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth()
                        )
                        ExposedDropdownMenu(
                            expanded = teamExpanded,
                            onDismissRequest = { teamExpanded = false }
                        ) {
                            teamResults.forEach { t ->
                                DropdownMenuItem(
                                    text = { Text(t) },
                                    onClick = {
                                        teamQuery = t
                                        teamExpanded = false
                                    }
                                )
                            }
                        }
                    }
                }
                
                var feeM by remember { mutableStateOf("") }
                var transferDate by remember { mutableStateOf("") }
                item {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(value = feeM, onValueChange = { feeM = it }, label = { Text("Fee (€M)") }, modifier = Modifier.weight(1f))
                        
                        var showDatePicker by remember { mutableStateOf(false) }
                        if (showDatePicker) {
                            val datePickerState = rememberDatePickerState()
                            DatePickerDialog(
                                onDismissRequest = { showDatePicker = false },
                                confirmButton = {
                                    TextButton(onClick = {
                                        datePickerState.selectedDateMillis?.let { millis ->
                                            val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
                                            transferDate = sdf.format(java.util.Date(millis))
                                        }
                                        showDatePicker = false
                                    }) { Text("OK") }
                                },
                                dismissButton = {
                                    TextButton(onClick = { showDatePicker = false }) { Text("Cancel") }
                                }
                            ) {
                                DatePicker(state = datePickerState)
                            }
                        }
                        
                        OutlinedTextField(
                            value = transferDate,
                            onValueChange = {},
                            label = { Text("Date") },
                            modifier = Modifier.weight(1f).clickable { showDatePicker = true },
                            enabled = false,
                            colors = OutlinedTextFieldDefaults.colors(
                                disabledTextColor = MaterialTheme.colorScheme.onSurface,
                                disabledBorderColor = MaterialTheme.colorScheme.outline,
                                disabledLabelColor = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        )
                    }
                }
                item {
                    Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth().padding(top = 16.dp)) {
                        TextButton(onClick = onDismiss) { Text("Cancel", color = Color.White) }
                        Button(onClick = {
                            viewModel.addTransferLog(com.example.TransferLog(
                                playerName = playerQuery,
                                type = transferType,
                                feeM = feeM.toDoubleOrNull() ?: 0.0,
                                fromToClub = teamQuery,
                                date = transferDate,
                                includeSwap = includeSwap,
                                isRegen = isRegen
                            ))
                            onDismiss()
                        }) { Text("Submit Transfer") }
                    }
                }
            }
        }
    }
}"""
text = re.sub(r'@Composable\s*fun TransferFormModal.*?\}\s*\}\s*\}', modal_replacement, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/TransfersScreen.kt', 'w') as f:
    f.write(text)
