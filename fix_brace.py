import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

bad = """            Icon(Icons.Default.Add, "Log Match", tint = MaterialTheme.colorScheme.onPrimary)
        }
        
        if (showMatchForm) {"""

good = """            Icon(Icons.Default.Add, "Log Match", tint = MaterialTheme.colorScheme.onPrimary)
        }
        }
        
        if (showMatchForm) {"""

content = content.replace(bad, good)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

