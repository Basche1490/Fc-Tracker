import re
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

old_data = """                    Button(onClick = { /* Reset */ }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                        Text("Reset All Active Save Data")
                    }
                }
            }"""

new_data = """                    Button(onClick = { /* Reset */ }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)) {
                        Text("Reset All Active Save Data")
                    }
                    
                    Spacer(Modifier.height(16.dp))
                    Button(
                        onClick = { viewModel.endSeason() }, 
                        modifier = Modifier.fillMaxWidth(), 
                        colors = ButtonDefaults.buttonColors(containerColor = com.example.ui.theme.WinColor)
                    ) {
                        Text("End Current Season & Archive Data")
                    }
                }
            }"""

content = content.replace(old_data, new_data)
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
