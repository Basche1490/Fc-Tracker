import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

print("import kotlinx.coroutines.delay" in content)
print("import com.google.gson.Gson" in content)
