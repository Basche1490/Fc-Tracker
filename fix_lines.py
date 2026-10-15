import sys
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if 'val lines = response.split("' in line:
        new_lines.append('                val lines = response.lines()\n')
        skip = True
        continue
    if skip and '")' in line:
        skip = False
        continue
    if skip:
        continue
    
    new_lines.append(line)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    for line in new_lines:
        f.write(line)
