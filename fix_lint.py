import re

file_path = "/app/applet/app/src/main/java/com/example/ui/screens/MatchesScreen.kt"
with open(file_path, "r") as f:
    text = f.read()

text = text.replace("while(newAssisters.size > newGoals) newAssisters.removeLast()", "while(newAssisters.size > newGoals) newAssisters.removeAt(newAssisters.lastIndex)")

with open(file_path, "w") as f:
    f.write(text)
