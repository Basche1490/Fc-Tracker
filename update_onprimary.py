import os

files = [
    "app/src/main/java/com/example/ui/screens/DashboardScreen.kt",
    "app/src/main/java/com/example/ui/screens/FormationTab.kt",
    "app/src/main/java/com/example/ui/screens/MatchesScreen.kt"
]

for file in files:
    with open(file, "r") as f:
        text = f.read()

    if "DashboardScreen" in file:
        text = text.replace('Text(state.clubName.take(1).uppercase(), fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color.White)', 'Text(state.clubName.take(1).uppercase(), fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onPrimary)')
    
    if "FormationTab" in file:
        text = text.replace('Text(player.squadNumber.toString(), fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color.White)', 'Text(player.squadNumber.toString(), fontSize = 10.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onPrimary)')
        # Wait, the grep output says: Text(player.number.toString() or squadNumber ? Let's check
    
    if "MatchesScreen" in file:
        text = text.replace('Text(state.clubName.take(1).uppercase(), fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color.White)', 'Text(state.clubName.take(1).uppercase(), fontSize = 24.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onPrimary)')

    with open(file, "w") as f:
        f.write(text)
