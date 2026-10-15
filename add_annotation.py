import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "fun ScoutNetworkTab(viewModel: com.example.MainViewModel, state: AppState, onDeployScout: () -> Unit, onManageNetwork: () -> Unit)",
    "@Composable\nfun ScoutNetworkTab(viewModel: com.example.MainViewModel, state: AppState, onDeployScout: () -> Unit, onManageNetwork: () -> Unit)"
)

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(content)
