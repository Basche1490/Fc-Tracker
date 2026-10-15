import re
with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

content = content.replace("@Composable\n@Composable\nfun TopProspectsWidget", "@Composable\nfun TopProspectsWidget")

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)
