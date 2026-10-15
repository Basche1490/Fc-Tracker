import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

text = text.replace('DialogProperties(usePlatformDefaultWidth = false)', 'DialogProperties(usePlatformDefaultWidth = false, decorFitsSystemWindows = false)')

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
