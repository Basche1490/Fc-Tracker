import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

# Add isPromoted to Player data class
if "val isPromoted: Boolean = false" not in content:
    content = content.replace(
        "val isRegen: Boolean = false,",
        "val isRegen: Boolean = false,\n    val isPromoted: Boolean = false,"
    )
    with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
        f.write(content)
    print("Added isPromoted")
