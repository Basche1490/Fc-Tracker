import re
with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

medical_tab = """@OptIn(androidx.compose.material3.ExperimentalMaterial3Api::class)
@Composable
fun MedicalWingTab(players: List<Player>, modifier: Modifier = Modifier) {
    var expanded by remember { mutableStateOf(false) }
    var selectedPlayer by remember { mutableStateOf<Player?>(null) }
    
    Column(modifier = modifier.fillMaxSize().padding(16.dp)) {
        DarkCard(modifier = Modifier.fillMaxWidth()) {
            Text("Add / Edit Injury", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
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
                        modifier = Modifier.fillMaxWidth().menuAnchor(),
                        trailingIcon = { androidx.compose.material3.ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) }
                    )
                    androidx.compose.material3.ExposedDropdownMenu(
                        expanded = expanded,
                        onDismissRequest = { expanded = false }
                    ) {
                        players.filter { !it.isAcademy }.forEach { player ->
                            androidx.compose.material3.DropdownMenuItem(
                                text = { Text(player.displayName) },
                                onClick = {
                                    selectedPlayer = player
                                    expanded = false
                                }
                            )
                        }
                    }
                }
                OutlinedTextField(
                    value = "",
                    onValueChange = {},
                    label = { Text("Injury Type (e.g. ACL Tear)") },
                    modifier = Modifier.fillMaxWidth()
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(value = "", onValueChange = {}, label = { Text("Start Date") }, modifier = Modifier.weight(1f))
                    OutlinedTextField(value = "", onValueChange = {}, label = { Text("Return Date") }, modifier = Modifier.weight(1f))
                }
                
                Spacer(Modifier.height(16.dp))
                Row(horizontalArrangement = Arrangement.End, modifier = Modifier.fillMaxWidth()) {
                    Button(onClick = { }) {
                        Text("Save Injury Record")
                    }
                }
            }
        }
    }
}"""

# Need to replace the old MedicalWingTab with the new one.
pattern = re.compile(r"@Composable\s+fun MedicalWingTab\(.*?\)\s*\{.*?(?=@Composable)", re.DOTALL)
content = re.sub(pattern, medical_tab + "\n\n", content)

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)
print("Updated MedicalWingTab")
