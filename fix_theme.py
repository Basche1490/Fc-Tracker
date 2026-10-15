import re

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "r") as f:
    text = f.read()

text = text.replace("import androidx.compose.ui.graphics.Color", "import androidx.compose.ui.graphics.Color\nimport androidx.compose.ui.graphics.luminance")

text = text.replace("onPrimary = Color.White,", "onPrimary = if (customPrimary.luminance() > 0.5f) Color.Black else Color.White,")

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write(text)
