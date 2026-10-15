import re

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.material.icons.filled.Person\n", "import androidx.compose.material.icons.filled.*\n")
content = content.replace("androidx.compose.material.icons.filled.DateRange", "Icons.Default.DateRange")

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)
