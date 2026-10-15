import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

# Replace padding on the Save Match Result button to have 48.dp bottom padding
text = text.replace('modifier = Modifier.fillMaxWidth().padding(16.dp)\n                ) {\n                    Text("Save Match Result", fontSize = 16.sp, fontWeight = FontWeight.Bold)\n                }', 'modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, top = 16.dp, bottom = 48.dp)\n                ) {\n                    Text("Save Match Result", fontSize = 16.sp, fontWeight = FontWeight.Bold)\n                }')

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
