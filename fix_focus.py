import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

if "import androidx.compose.ui.platform.LocalFocusManager" not in content:
    content = content.replace("import androidx.compose.ui.platform.LocalContext", "import androidx.compose.ui.platform.LocalContext\nimport androidx.compose.ui.platform.LocalFocusManager")

# Add focusManager to MainScreen
insert_focus_manager = """    val focusManager = LocalFocusManager.current
    LaunchedEffect(drawerState.isOpen) {
        if (drawerState.isOpen) {
            focusManager.clearFocus()
        }
    }
"""
content = content.replace("val navController = rememberNavController()", "val navController = rememberNavController()\n" + insert_focus_manager)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

