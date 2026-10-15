import re

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

content = content.replace("@Composable\n@Composable\nfun ObjectivesWidget", "@Composable\nfun ObjectivesWidget")

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "r") as f:
    content = f.read()

content = content.replace("androidx.compose.material.icons.Icons.Default.ArrowDropDown", "androidx.compose.material.icons.Icons.Default.ArrowDropDown")
content = content.replace("androidx.compose.material.icons.Icons.Default.ArrowDropDown", "androidx.compose.material.icons.filled.ArrowDropDown")

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

content = content.replace("startYear = state.startYear", "startYear = viewModel.state.value.startYear")

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)
