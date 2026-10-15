import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

old_add_transfer = r"""    fun addTransferLog\(log: TransferLog\) \{
        _state\.update \{ it\.copy\(transfers = it\.transfers \+ log\) \}
    \}"""

new_add_transfer = """    fun addTransferLog(log: TransferLog) {
        _state.update { state ->
            val updatedPlayers = state.players.map { player ->
                if (player.name == log.playerName || player.displayName == log.playerName) {
                    when (log.type) {
                        "Out (Permanent)" -> player.copy(status = "Sold")
                        "Out (Loan)" -> player.copy(status = "Loaned Out", isLoanedOut = true, isStartingXI = false)
                        "In (Loan)" -> player.copy(isLoanedIn = true)
                        else -> player
                    }
                } else {
                    player
                }
            }
            state.copy(transfers = state.transfers + log, players = updatedPlayers)
        }
    }"""

content = re.sub(old_add_transfer, new_add_transfer, content)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
