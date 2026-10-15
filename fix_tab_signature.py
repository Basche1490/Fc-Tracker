import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

target1 = "fun TransferMarketTab(state: AppState, displayTransfers: List<com.example.TransferLog>, onLogTransfer: () -> Unit, viewModel: com.example.MainViewModel) {"
rep1 = "fun TransferMarketTab(state: AppState, displayTransfers: List<com.example.TransferLog>, onLogTransfer: () -> Unit, viewModel: com.example.MainViewModel, onEditTransfer: (com.example.TransferLog) -> Unit = {}) {"
if target1 in content:
    content = content.replace(target1, rep1)

target2 = "0 -> TransferMarketTab(state, displayTransfers, onLogTransfer = { showTransferForm = true }, viewModel = viewModel)"
rep2 = "0 -> TransferMarketTab(state, displayTransfers, onLogTransfer = { showTransferForm = true }, viewModel = viewModel, onEditTransfer = { logToEdit = it })"
if target2 in content:
    content = content.replace(target2, rep2)

target3 = ".clickable { logToEdit = log }"
rep3 = ".clickable { onEditTransfer(log) }"
if target3 in content:
    content = content.replace(target3, rep3)

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(content)

