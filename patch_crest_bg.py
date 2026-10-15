import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_bg = r"modifier = modifier\.background\(Color\.White\),"
new_bg = "modifier = modifier,"
content = re.sub(old_bg, new_bg, content)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
