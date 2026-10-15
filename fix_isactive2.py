import sys
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("import isActive", "import kotlinx.coroutines.isActive")

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
