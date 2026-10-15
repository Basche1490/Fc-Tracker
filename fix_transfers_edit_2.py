import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

target = "    if (showTransferForm) TransferFormModal(state = viewModel.state.collectAsState().value, viewModel = viewModel) { showTransferForm = false }"
replacement = """    if (showTransferForm) TransferFormModal(state = viewModel.state.collectAsState().value, viewModel = viewModel, logToEdit = null) { showTransferForm = false }
    if (logToEdit != null) TransferFormModal(state = viewModel.state.collectAsState().value, viewModel = viewModel, logToEdit = logToEdit) { logToEdit = null }"""
if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
        f.write(content)
    print("Fixed showTransferForm Modal")
else:
    print("Could not find showTransferForm")

