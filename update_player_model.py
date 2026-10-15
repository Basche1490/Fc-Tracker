import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

old_player = r"val isInjured: Boolean = false,"
new_player = """val isInjured: Boolean = false,
    val injuryName: String? = null,
    val injuryStartDate: String? = null,
    val injuryReturnDate: String? = null,"""
content = re.sub(old_player, new_player, content)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
