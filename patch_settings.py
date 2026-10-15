import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

color_picker_imports = """
import androidx.compose.ui.window.Dialog
"""
if "androidx.compose.ui.window.Dialog" not in content:
    content = content.replace("import androidx.compose.ui.unit.sp", "import androidx.compose.ui.unit.sp\n" + color_picker_imports)

old_colors = """                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(value = primaryColorHex, onValueChange = { primaryColorHex = it }, label = { Text("Primary Color") }, modifier = Modifier.weight(1f), singleLine = true)
                        OutlinedTextField(value = secondaryColorHex, onValueChange = { secondaryColorHex = it }, label = { Text("Secondary Color") }, modifier = Modifier.weight(1f), singleLine = true)
                    }"""

new_colors = """                    var showPrimaryColorPicker by remember { mutableStateOf(false) }
                    var showSecondaryColorPicker by remember { mutableStateOf(false) }

                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = primaryColorHex, 
                            onValueChange = { primaryColorHex = it }, 
                            label = { Text("Primary Color") }, 
                            modifier = Modifier.weight(1f), 
                            singleLine = true,
                            trailingIcon = {
                                IconButton(onClick = { showPrimaryColorPicker = true }) {
                                    Icon(Icons.Default.Edit, contentDescription = "Pick Color")
                                }
                            }
                        )
                        OutlinedTextField(
                            value = secondaryColorHex, 
                            onValueChange = { secondaryColorHex = it }, 
                            label = { Text("Secondary Color") }, 
                            modifier = Modifier.weight(1f), 
                            singleLine = true,
                            trailingIcon = {
                                IconButton(onClick = { showSecondaryColorPicker = true }) {
                                    Icon(Icons.Default.Edit, contentDescription = "Pick Color")
                                }
                            }
                        )
                    }
                    
                    if (showPrimaryColorPicker) {
                        Dialog(onDismissRequest = { showPrimaryColorPicker = false }) {
                            DarkCard(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Text("Select Primary Color", color = Color.White, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(16.dp))
                                Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
                                    ColorWheel(modifier = Modifier.fillMaxSize()) { color ->
                                        primaryColorHex = color.toHexCode()
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Button(onClick = { showPrimaryColorPicker = false }, modifier = Modifier.fillMaxWidth()) {
                                    Text("Done")
                                }
                            }
                        }
                    }
                    if (showSecondaryColorPicker) {
                        Dialog(onDismissRequest = { showSecondaryColorPicker = false }) {
                            DarkCard(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Text("Select Secondary Color", color = Color.White, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(16.dp))
                                Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
                                    ColorWheel(modifier = Modifier.fillMaxSize()) { color ->
                                        secondaryColorHex = color.toHexCode()
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Button(onClick = { showSecondaryColorPicker = false }, modifier = Modifier.fillMaxWidth()) {
                                    Text("Done")
                                }
                            }
                        }
                    }"""

content = content.replace(old_colors, new_colors)

old_saves = """                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(onClick = { /* Switch to Slot 1 */ }, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)) {
                            Text("Save Slot 1 (Active)")
                        }
                        Button(onClick = { /* Switch to Slot 2 */ }, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) {
                            Text("Save Slot 2", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }"""

new_saves = """                    var showNewSavePrompt by remember { mutableStateOf<Int?>(null) }
                    
                    val activeSlot = viewModel.activeSaveSlot
                    val slot1Name = viewModel.saveSlotNames[1] ?: "Save Slot 1"
                    val slot2Name = viewModel.saveSlotNames[2] ?: "Save Slot 2"
                    
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Button(
                            onClick = { 
                                if (activeSlot != 1) {
                                    if (viewModel.saveSlots.containsKey(1)) {
                                        viewModel.switchSaveSlot(1)
                                    } else {
                                        showNewSavePrompt = 1
                                    }
                                }
                            }, 
                            modifier = Modifier.weight(1f), 
                            colors = ButtonDefaults.buttonColors(containerColor = if (activeSlot == 1) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Text(slot1Name + if(activeSlot == 1) " (Active)" else "", color = if (activeSlot == 1) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        Button(
                            onClick = { 
                                if (activeSlot != 2) {
                                    if (viewModel.saveSlots.containsKey(2)) {
                                        viewModel.switchSaveSlot(2)
                                    } else {
                                        showNewSavePrompt = 2
                                    }
                                }
                            }, 
                            modifier = Modifier.weight(1f), 
                            colors = ButtonDefaults.buttonColors(containerColor = if (activeSlot == 2) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Text(slot2Name + if(activeSlot == 2) " (Active)" else "", color = if (activeSlot == 2) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                    
                    if (showNewSavePrompt != null) {
                        androidx.compose.material3.AlertDialog(
                            onDismissRequest = { showNewSavePrompt = null },
                            title = { Text("Create New Save?") },
                            text = { Text("This slot is empty. Do you want to create a new save?") },
                            confirmButton = {
                                Button(onClick = {
                                    val slotToCreate = showNewSavePrompt!!
                                    showNewSavePrompt = null
                                    viewModel.switchSaveSlot(slotToCreate, createNew = true)
                                }) {
                                    Text("Yes")
                                }
                            },
                            dismissButton = {
                                androidx.compose.material3.TextButton(onClick = { showNewSavePrompt = null }) {
                                    Text("No")
                                }
                            }
                        )
                    }"""

content = content.replace(old_saves, new_saves)

old_buttons = """                    Button(onClick = { /* Reset */ }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                        Text("Reset All Active Save Data")
                    }
                    
                    Spacer(Modifier.height(16.dp))
                    Button(
                        onClick = { viewModel.endSeason() }, 
                        modifier = Modifier.fillMaxWidth(), 
                        colors = ButtonDefaults.buttonColors(containerColor = com.example.ui.theme.WinColor)
                    ) {
                        Text("End Current Season & Archive Data")
                    }"""

new_buttons = """                    Button(onClick = { viewModel.deleteCurrentSave() }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                        Text("Delete Current Save")
                    }"""

content = content.replace(old_buttons, new_buttons)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)

