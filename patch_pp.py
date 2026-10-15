import re
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

old_pp = """    val shotAccuracy: Int = 0,
    val saves: Int = 0,"""

new_pp = """    val shotAccuracy: Int = 0,
    val saves: Int = 0,
    val tackles: Int = 0,
    val interceptions: Int = 0,"""

content = content.replace(old_pp, new_pp)
with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
