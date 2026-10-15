import re

def rewrite():
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
        content = f.read()

    content = content.replace("import androidx.compose.ui.layout.boundsInWindow", "import androidx.compose.ui.layout.boundsInRoot")
    content = content.replace("import androidx.compose.ui.layout.positionInWindow", "import androidx.compose.ui.layout.positionInRoot")

    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
        f.write(content)

rewrite()
