import sys
with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        if "}" in line:
            skip_next = False
        continue

    # Identify the injected LaunchedEffect that wasn't supposed to be there (outside of DashboardScreen)
    if "androidx.compose.runtime.LaunchedEffect(Unit) {" in line:
        # Check if we are inside DashboardScreen
        # We can just check the previous line
        if "val displayPlayers" in lines[i-1]:
            # Keep only if inside DashboardScreen (approx around line 45-50)
            if i > 100:
                skip_next = True
                continue
    
    new_lines.append(line)

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    for line in new_lines:
        f.write(line)
