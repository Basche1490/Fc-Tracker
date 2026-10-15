import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

old_saves = """                        Button(
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
                    }"""

new_saves = """                        Button(
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
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    var renameText by remember(activeSlot, viewModel.saveSlotNames) { mutableStateOf(viewModel.saveSlotNames[activeSlot] ?: "") }
                    Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = renameText,
                            onValueChange = { renameText = it },
                            label = { Text("Active Save Name") },
                            modifier = Modifier.weight(1f),
                            singleLine = true
                        )
                        Button(onClick = { viewModel.renameSaveSlot(activeSlot, renameText) }) {
                            Text("Rename")
                        }
                    }"""

if 'label = { Text("Active Save Name") }' not in content:
    content = content.replace(old_saves, new_saves)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)

