import re

# 1. MainViewModel.kt
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

# Check if _state or _uiState is used
if "private val _state" in content:
    content = content.replace("_uiState.value", "_state.value")
elif "private val _uiState" in content:
    pass
else:
    content = content.replace("_uiState.value", "state.value")

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)

# 2. AcademyScreen.kt
with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.foundation.clickable" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.clickable")

with open("app/src/main/java/com/example/ui/screens/AcademyScreen.kt", "w") as f:
    f.write(content)

# 3. AssistantScreen.kt
with open("app/src/main/java/com/example/ui/screens/AssistantScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.foundation.clickable" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.clickable")

with open("app/src/main/java/com/example/ui/screens/AssistantScreen.kt", "w") as f:
    f.write(content)

# 4. MatchesScreen.kt
with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

if "import java.util.TimeZone" not in content:
    content = content.replace("import java.util.Locale", "import java.util.Locale\nimport java.util.TimeZone")

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

# 5. TransfersScreen.kt
with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

content = content.replace("ScoutNetworkModal { showScoutNetworkModal = false }", "ScoutNetworkModal(onDismiss = { showScoutNetworkModal = false })")
# Wait, let's see if there is another DeployScoutModal call:
content = content.replace("DeployScoutModal { showDeployScoutModal = false }", "DeployScoutModal(allEafcPlayers = emptyList(), onDismiss = { showDeployScoutModal = false }, onSave = {})")

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(content)
