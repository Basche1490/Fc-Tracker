with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    lines = f.readlines()

# insert '}' at line 157
lines.insert(157, "}\n")

# remove last line if it's '}'
if lines[-1].strip() == "}":
    lines.pop()

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.writelines(lines)
