with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

text = text.replace('Text(initials, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)', 'Text(initials, color = if (bgColor == MaterialTheme.colorScheme.primary) MaterialTheme.colorScheme.onPrimary else Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)')

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
