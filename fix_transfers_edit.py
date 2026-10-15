import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

# 1. Add logToEdit state and pass it to TransferFormModal
if "var logToEdit by remember { mutableStateOf<com.example.TransferLog?>(null) }" not in content:
    content = content.replace(
        "var showTransferForm by remember { mutableStateOf(false) }",
        "var showTransferForm by remember { mutableStateOf(false) }\n    var logToEdit by remember { mutableStateOf<com.example.TransferLog?>(null) }"
    )
    
    # Show TransferFormModal for editing
    content = content.replace(
        "if (showTransferForm) TransferFormModal(state, viewModel, onDismiss = { showTransferForm = false })",
        "if (showTransferForm) TransferFormModal(state, viewModel, logToEdit = null, onDismiss = { showTransferForm = false })\n        if (logToEdit != null) TransferFormModal(state, viewModel, logToEdit = logToEdit, onDismiss = { logToEdit = null })"
    )
    
    # Make the TransferLog row clickable
    target_row = """                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .background(MaterialTheme.colorScheme.surface)
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {"""
    replacement_row = """                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(12.dp))
                                .background(MaterialTheme.colorScheme.surface)
                                .clickable { logToEdit = log }
                                .padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {"""
    content = content.replace(target_row, replacement_row)
    
    # Update TransferFormModal signature and initialization
    target_sig = """@Composable
fun TransferFormModal(state: com.example.AppState, viewModel: com.example.MainViewModel, onDismiss: () -> Unit) {
    var typeExpanded by remember { mutableStateOf(false) }
    var transferType by remember { mutableStateOf("In (Permanent)") }
    val transferTypes = listOf("In (Permanent)", "Out (Permanent)", "In (Loan)", "Out (Loan)", "Free Agent Sign")
    
    var playerQuery by remember { mutableStateOf("") }
    var searchResults by remember { mutableStateOf(emptyList<com.example.EafcPlayer>()) }
    var searchExpanded by remember { mutableStateOf(false) }
    
    var includeSwap by remember { mutableStateOf(false) }
    var isRegen by remember { mutableStateOf(false) }
    var swapPlayerQuery by remember { mutableStateOf("") }
    var swapSearchResults by remember { mutableStateOf(emptyList<com.example.EafcPlayer>()) }
    var swapSearchExpanded by remember { mutableStateOf(false) }
    
    var teamQuery by remember { mutableStateOf("") }
    var teamResults by remember { mutableStateOf(emptyList<String>()) }
    var teamExpanded by remember { mutableStateOf(false) }
    
    var feeM by remember { mutableStateOf("") }
    var transferDate by remember { mutableStateOf("") }
    var showDatePicker by remember { mutableStateOf(false) }"""

    replacement_sig = """@Composable
fun TransferFormModal(state: com.example.AppState, viewModel: com.example.MainViewModel, logToEdit: com.example.TransferLog? = null, onDismiss: () -> Unit) {
    var typeExpanded by remember { mutableStateOf(false) }
    var transferType by remember { mutableStateOf(logToEdit?.type ?: "In (Permanent)") }
    val transferTypes = listOf("In (Permanent)", "Out (Permanent)", "In (Loan)", "Out (Loan)", "Free Agent Sign")
    
    var playerQuery by remember { mutableStateOf(logToEdit?.playerName ?: "") }
    var searchResults by remember { mutableStateOf(emptyList<com.example.EafcPlayer>()) }
    var searchExpanded by remember { mutableStateOf(false) }
    
    var includeSwap by remember { mutableStateOf(logToEdit?.includeSwap ?: false) }
    var isRegen by remember { mutableStateOf(logToEdit?.isRegen ?: false) }
    var swapPlayerQuery by remember { mutableStateOf("") }
    var swapSearchResults by remember { mutableStateOf(emptyList<com.example.EafcPlayer>()) }
    var swapSearchExpanded by remember { mutableStateOf(false) }
    
    var teamQuery by remember { mutableStateOf(logToEdit?.fromToClub ?: "") }
    var teamResults by remember { mutableStateOf(emptyList<String>()) }
    var teamExpanded by remember { mutableStateOf(false) }
    
    var feeM by remember { mutableStateOf(logToEdit?.feeM?.toString() ?: "") }
    var transferDate by remember { mutableStateOf(logToEdit?.date ?: "") }
    var showDatePicker by remember { mutableStateOf(false) }"""
    content = content.replace(target_sig, replacement_sig)

    # Update Submit button to handle Edit vs Add and add Delete button
    target_submit = """                item {
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
                }"""
    replacement_submit = """                item {
                    Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth().padding(top = 16.dp)) {
                        if (logToEdit != null) {
                            Button(onClick = {
                                viewModel.deleteTransferLog(logToEdit.id)
                                onDismiss()
                            }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) { Text("Delete") }
                        } else {
                            Spacer(Modifier.width(8.dp))
                        }
                        
                        Row {
                            TextButton(onClick = onDismiss) { Text("Cancel", color = Color.White) }
                            Button(onClick = {
                                if (logToEdit != null) {
                                    viewModel.deleteTransferLog(logToEdit.id)
                                }
                                viewModel.addTransferLog(com.example.TransferLog(
                                    id = logToEdit?.id ?: java.util.UUID.randomUUID().toString(),
                                    playerName = playerQuery,
                                    type = transferType,
                                    feeM = feeM.toDoubleOrNull() ?: 0.0,
                                    fromToClub = teamQuery,
                                    date = transferDate,
                                    includeSwap = includeSwap,
                                    isRegen = isRegen
                                ))
                                onDismiss()
                            }) { Text(if (logToEdit != null) "Update" else "Submit") }
                        }
                    }
                }"""
    content = content.replace(target_submit, replacement_submit)

    with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
        f.write(content)
    print("Added edit/delete to TransfersScreen")

