import sys

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    lines = f.readlines()

new_lines = lines[:157] + lines[226:]

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.writelines(new_lines)
