import re

# 1. Fix AcademyScreen.kt playerToEdit missing
with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "r") as f:
    content = f.read()

if "var playerToEdit" not in content:
    content = content.replace(
        "var showYouthForm by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }",
        "var showYouthForm by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }\n    var playerToEdit by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf<com.example.Player?>(null) }"
    )

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "w") as f:
    f.write(content)

# 2. Fix TransfersScreen.kt lines 98 and 99 (and 92)
with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

# line 92: ScoutNetworkTab(state, ...) -> ScoutNetworkTab(viewModel, state, ...)
content = content.replace("ScoutNetworkTab(state, onDeployScout", "ScoutNetworkTab(viewModel, state, onDeployScout")

# line 98: DeployScoutModal(...)
content = content.replace("DeployScoutModal(viewModel.allEafcPlayers) { showDeployScout = false }", "DeployScoutModal(allEafcPlayers = viewModel.allEafcPlayers, onDismiss = { showDeployScout = false }, onSave = { report -> viewModel.addScoutReport(report); showDeployScout = false })")

# line 99: ScoutNetworkModal(...)
content = content.replace("ScoutNetworkModal { showScoutNetwork = false }", "ScoutNetworkModal(onDismiss = { showScoutNetwork = false })")

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(content)

print("Finished fixing final issues")
