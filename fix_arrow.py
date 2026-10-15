import re
with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "r") as f:
    content = f.read()

content = content.replace("Icon(androidx.compose.material.icons.filled.ArrowDropDown, \"\")", "Text(\"▼\", modifier = Modifier.padding(start=4.dp))")

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "w") as f:
    f.write(content)
