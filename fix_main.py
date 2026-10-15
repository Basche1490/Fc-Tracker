with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Add imports
imports = """import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.runtime.LaunchedEffect
"""
content = content.replace("import kotlinx.coroutines.launch", "import kotlinx.coroutines.launch\n" + imports)

# Move FocusManager and LaunchedEffect down
bad_block = """    val focusManager = LocalFocusManager.current
    LaunchedEffect(drawerState.isOpen) {
        if (drawerState.isOpen) {
            focusManager.clearFocus()
        }
    }"""
content = content.replace(bad_block, "")

# Insert below drawerState definition
correct_block = """        val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
        val scope = rememberCoroutineScope()
        
        val focusManager = LocalFocusManager.current
        LaunchedEffect(drawerState.isOpen) {
            if (drawerState.isOpen) {
                focusManager.clearFocus()
            }
        }"""
content = content.replace("        val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)\n        val scope = rememberCoroutineScope()", correct_block)


with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
