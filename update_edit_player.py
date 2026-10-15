import re

with open('app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt', 'r') as f:
    text = f.read()

# Add isRegen to EditPlayerDialog
text = text.replace('var weakFoot by remember { mutableStateOf(player?.weakFoot?.toString() ?: "3") }', 'var weakFoot by remember { mutableStateOf(player?.weakFoot?.toString() ?: "3") }\n    var isRegen by remember { mutableStateOf(player?.isRegen ?: false) }')

is_regen_row = """                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = isRegen, onCheckedChange = { isRegen = it })
                    Text("Is Regen", color = Color.White)
                }"""

text = text.replace('                OutlinedTextField(value = nationality, onValueChange = { nationality = it }, label = { Text("Nationality") }, modifier = Modifier.fillMaxWidth())', is_regen_row + '\n                OutlinedTextField(value = nationality, onValueChange = { nationality = it }, label = { Text("Nationality") }, modifier = Modifier.fillMaxWidth())')

# Add DatePicker to EditPlayerDialog
date_picker = """                var showDatePicker by remember { mutableStateOf(false) }
                if (showDatePicker) {
                    val datePickerState = rememberDatePickerState()
                    DatePickerDialog(
                        onDismissRequest = { showDatePicker = false },
                        confirmButton = {
                            TextButton(onClick = {
                                datePickerState.selectedDateMillis?.let { millis ->
                                    val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
                                    birthDate = sdf.format(java.util.Date(millis))
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
                    value = birthDate,
                    onValueChange = {},
                    label = { Text("Birth Date") },
                    modifier = Modifier.fillMaxWidth().clickable { showDatePicker = true },
                    enabled = false,
                    colors = OutlinedTextFieldDefaults.colors(
                        disabledTextColor = MaterialTheme.colorScheme.onSurface,
                        disabledBorderColor = MaterialTheme.colorScheme.outline,
                        disabledLabelColor = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                )"""

text = text.replace('                OutlinedTextField(value = birthDate, onValueChange = { birthDate = it }, label = { Text("Birth Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())', date_picker)

# Add isRegen to the Player constructor calls
text = text.replace('headshotUrl = headshotUrl\n                        ) ?: Player(', 'headshotUrl = headshotUrl,\n                            isRegen = isRegen\n                        ) ?: Player(')
text = text.replace('headshotUrl = headshotUrl\n                        )\n                        onUpdate(newPlayer)', 'headshotUrl = headshotUrl,\n                            isRegen = isRegen\n                        )\n                        onUpdate(newPlayer)')

# Add missing imports for DatePicker if they don't exist
if 'import androidx.compose.material3.DatePicker' not in text:
    text = text.replace('import androidx.compose.material3.Text', 'import androidx.compose.material3.*\nimport androidx.compose.foundation.clickable\nimport androidx.compose.material3.Text')

with open('app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt', 'w') as f:
    f.write(text)
