import sys
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    lines = f.readlines()

out = []
out.append("package com.example\n")
out.append("import kotlinx.coroutines.isActive\n")
for line in lines:
    if line.strip() == "import kotlinx.coroutines.isActive":
        continue
    if line.strip() == "package com.example":
        continue
    out.append(line)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    for line in out:
        f.write(line)
