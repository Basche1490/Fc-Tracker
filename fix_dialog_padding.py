import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

# Replace padding(16.dp) on the button with explicit larger bottom padding
text = text.replace('modifier = Modifier.fillMaxWidth().padding(16.dp)', 'modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, top = 16.dp, bottom = 48.dp)')

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
