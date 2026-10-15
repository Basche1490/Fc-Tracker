import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# Replace passing and shooting fields
old_passing_shooting = """        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedTextField(
                value = perf.passAccuracy.toString(),
                onValueChange = { onUpdate(perf.copy(passAccuracy = it.toIntOrNull() ?: 0)) },
                label = { Text("Pass Acc (%)") },
                modifier = Modifier.weight(1f),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
        }
        
        if (!isGk) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = perf.shotAccuracy.toString(),
                    onValueChange = { onUpdate(perf.copy(shotAccuracy = it.toIntOrNull() ?: 0)) },
                    label = { Text("Shot Acc (%)") },
                    modifier = Modifier.weight(1f),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
            }
        }"""

new_passing_shooting = """        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            OutlinedTextField(
                value = perf.passes.toString(),
                onValueChange = { onUpdate(perf.copy(passes = it.toIntOrNull() ?: 0)) },
                label = { Text("Passes") },
                modifier = Modifier.weight(1f),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
            OutlinedTextField(
                value = perf.passAccuracy.toString(),
                onValueChange = { onUpdate(perf.copy(passAccuracy = it.toIntOrNull() ?: 0)) },
                label = { Text("Pass Acc (%)") },
                modifier = Modifier.weight(1f),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
            )
        }
        
        if (!isGk) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = perf.shots.toString(),
                    onValueChange = { onUpdate(perf.copy(shots = it.toIntOrNull() ?: 0)) },
                    label = { Text("Shots") },
                    modifier = Modifier.weight(1f),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
                OutlinedTextField(
                    value = perf.shotAccuracy.toString(),
                    onValueChange = { onUpdate(perf.copy(shotAccuracy = it.toIntOrNull() ?: 0)) },
                    label = { Text("Shot Acc (%)") },
                    modifier = Modifier.weight(1f),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
                )
            }
        }"""

if "value = perf.passes.toString()" not in content:
    content = content.replace(old_passing_shooting, new_passing_shooting)

# Replace cards logic
old_cards = """        Row(horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = perf.yellowCard, onCheckedChange = { onUpdate(perf.copy(yellowCard = it)) })
                Text("Yellow", fontSize = 12.sp, color = Color.White)
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = perf.redCard, onCheckedChange = { onUpdate(perf.copy(redCard = it)) })
                Text("Red", fontSize = 12.sp, color = Color.White)
            }
            if (isGk || isDef) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = perf.cleanSheet, onCheckedChange = { onUpdate(perf.copy(cleanSheet = it)) })
                    Text("Clean Sheet", fontSize = 12.sp, color = Color.White)
                }
            }
        }"""

new_cards = """        Row(horizontalArrangement = if (isGk || isDef) Arrangement.SpaceBetween else Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = perf.yellowCard, onCheckedChange = { onUpdate(perf.copy(yellowCard = it)) })
                Text("Yellow", fontSize = 12.sp, color = Color.White)
            }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(checked = perf.redCard, onCheckedChange = { onUpdate(perf.copy(redCard = it)) })
                Text("Red", fontSize = 12.sp, color = Color.White)
            }
            if (isGk || isDef) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Checkbox(checked = perf.cleanSheet, onCheckedChange = { onUpdate(perf.copy(cleanSheet = it)) })
                    Text("Clean Sheet", fontSize = 12.sp, color = Color.White)
                }
            }
        }"""

content = content.replace(old_cards, new_cards)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

