import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("val saveSlotNames = mutableMapOf<Int, String>()", "val saveSlotNames = androidx.compose.runtime.mutableStateMapOf<Int, String>()")

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
