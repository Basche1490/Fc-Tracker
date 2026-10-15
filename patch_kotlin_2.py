import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    code = f.read()

# Update parseMatchPerformances
code = re.sub(
    r'assists = p\.optInt\("assists"\),\s+rating = 0\.0\s+\)\)',
    r'assists = p.optInt("assists")\n        ))',
    code
)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(code)

print("Patched MainViewModel 2!")
