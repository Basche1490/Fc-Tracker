import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

text = re.sub(r'value = matchDate,\s*onValueChange = \{\},', 'value = matchDate.ifEmpty { "YYYY-MM-DD" },\n                                onValueChange = {},', text)

text = text.replace('placeholder = { Text("YYYY-MM-DD") },\n', '')

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
