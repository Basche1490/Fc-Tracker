import re

with open("app/src/main/java/com/example/ui/screens/EditYouthPlayerDialog.kt", "r") as f:
    content = f.read()

# Fix signature
content = content.replace(
    "fun EditYouthPlayerDialog(player: Player? = null, onDismiss: () -> Unit, onUpdate: (Player) -> Unit, onDelete: (() -> Unit)? = null) {",
    "fun EditYouthPlayerDialog(startYear: Int = 2025, player: Player? = null, onDismiss: () -> Unit, onUpdate: (Player) -> Unit, onDelete: (() -> Unit)? = null) {"
)

# Add LaunchedEffect
launched_effect = """
    LaunchedEffect(birthDate, startYear) {
        try {
            val parts = birthDate.split("-")
            if (parts.size >= 1) {
                val birthYear = parts[0].toInt()
                age = (startYear - birthYear).toString()
            }
        } catch(e: Exception) {}
    }
"""

content = content.replace(
    "val weakFootOptions = listOf(\"1\", \"2\", \"3\", \"4\", \"5\")",
    "val weakFootOptions = listOf(\"1\", \"2\", \"3\", \"4\", \"5\")" + launched_effect
)

# Remove the old Age field Row
old_age_row = """                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(value = age, onValueChange = { age = it }, label = { Text("Age") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.weight(1f))
                }"""
content = content.replace(old_age_row, "")

# Add Age below Birth Date
new_age = """                OutlinedTextField(value = birthDate, onValueChange = { birthDate = it }, label = { Text("Birth Date (YYYY-MM-DD)") }, modifier = Modifier.fillMaxWidth())
                OutlinedTextField(value = age, onValueChange = { age = it }, label = { Text("Age (Auto)") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.fillMaxWidth(), readOnly = true, colors = OutlinedTextFieldDefaults.colors(disabledTextColor = MaterialTheme.colorScheme.onSurfaceVariant, disabledBorderColor = MaterialTheme.colorScheme.outline, disabledLabelColor = MaterialTheme.colorScheme.onSurfaceVariant))"""

content = content.replace("                OutlinedTextField(value = birthDate, onValueChange = { birthDate = it }, label = { Text(\"Birth Date (YYYY-MM-DD)\") }, modifier = Modifier.fillMaxWidth())", new_age)

with open("app/src/main/java/com/example/ui/screens/EditYouthPlayerDialog.kt", "w") as f:
    f.write(content)
