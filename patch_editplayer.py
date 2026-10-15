import re

with open("app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt", "r") as f:
    content = f.read()

# Pass startYear to EditPlayerDialog
content = content.replace("fun EditPlayerDialog(", "fun EditPlayerDialog(startYear: Int = 2025, ")

# Compute age dynamically
age_logic = """
    // Compute age dynamically
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

content = content.replace("var birthDate by remember { mutableStateOf(player?.birthDate ?: \"2000-01-01\") }", "var birthDate by remember { mutableStateOf(player?.birthDate ?: \"2000-01-01\") }\n" + age_logic)

# Replace the row with age, startingOverall, overall
old_row = """                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(value = age, onValueChange = { age = it }, label = { Text("Age") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.weight(1f))
                    OutlinedTextField(value = startingOverall, onValueChange = { startingOverall = it }, label = { Text("Start OVR") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.weight(1f))
                    OutlinedTextField(value = overall, onValueChange = { overall = it }, label = { Text("Overall") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.weight(1f))
                }"""

new_row = """                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(value = age, onValueChange = { age = it }, label = { Text("Age (Auto)") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.weight(1f), readOnly = true)
                    OutlinedTextField(value = startingOverall, onValueChange = { startingOverall = it }, label = { Text("Starting OVR") }, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), modifier = Modifier.weight(1f))
                }"""

content = content.replace(old_row, new_row)

# Update the save logic to use startingOverall for overall IF it's a new player, or retain the existing overall if it's an edit
# But wait! If we retain existing overall, how does the user update overall? Oh, they might train the player in the app? (Not implemented, but maybe).
# I'll just change `overall = overall.toIntOrNull() ?: 60` to `overall = player?.overall ?: (startingOverall.toIntOrNull() ?: 60)`

content = content.replace("overall = overall.toIntOrNull() ?: 60", "overall = player?.overall ?: (startingOverall.toIntOrNull() ?: 60)")

with open("app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt", "w") as f:
    f.write(content)

