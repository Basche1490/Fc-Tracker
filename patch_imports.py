with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.material.icons.filled.Edit" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Menu", "import androidx.compose.material.icons.filled.Menu\nimport androidx.compose.material.icons.filled.Edit")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
