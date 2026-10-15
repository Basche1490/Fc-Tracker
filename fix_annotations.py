import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

# Fix duplicate @Composable for ScoutNetworkTab
content = content.replace(
    "@Composable\n@Composable\nfun ScoutNetworkTab",
    "@Composable\nfun ScoutNetworkTab"
)

# Fix missing @Composable for TransferFormModal
content = content.replace(
    "@OptIn(ExperimentalMaterial3Api::class)\nfun TransferFormModal",
    "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun TransferFormModal"
)

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(content)
