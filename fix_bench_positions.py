with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
    content = f.read()

# Add benchPositions
old_state = "var selectedFormation by remember { mutableStateOf(\"4-3-3\") }"
new_state = """var selectedFormation by remember { mutableStateOf("4-3-3") }
    val benchPositions = remember { androidx.compose.runtime.mutableStateMapOf<String, androidx.compose.ui.geometry.Offset>() }"""
content = content.replace(old_state, new_state)

with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
    f.write(content)
