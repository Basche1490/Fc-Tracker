import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    code = f.read()

# Replace the substitution Minute OutlinedTextField
code = re.sub(
    r'OutlinedTextField\(\s+value = subMinute,\s+onValueChange = { subMinute = it },\s+label = { Text\("Minute"\) },\s+modifier = Modifier\.weight\(1f\),\s+keyboardOptions = KeyboardOptions\(keyboardType = KeyboardType\.Number\)\s+\)',
    '',
    code
)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(code)

print("Patched Subs!")
