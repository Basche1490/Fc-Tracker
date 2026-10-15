import re

with open('app/src/main/java/com/example/MainViewModel.kt', 'r') as f:
    text = f.read()

# Add teamCrestUrl to TransferLog
transfer_log = """data class TransferLog(
    val id: String = java.util.UUID.randomUUID().toString(),
    val playerName: String,
    val type: String,
    val feeM: Double,
    val fromToClub: String,
    val date: String = "",
    val includeSwap: Boolean = false,
    val isRegen: Boolean = false
)"""
text = re.sub(r'data class TransferLog\(.*?val fromToClub: String\n\)', transfer_log, text, flags=re.DOTALL)

# Add addTransferLog method
add_method = """    fun addObjective(objective: Objective) {
        _state.update { it.copy(objectives = it.objectives + objective) }
    }

    fun addTransferLog(log: TransferLog) {
        _state.update { it.copy(transfers = it.transfers + log) }
    }"""
text = text.replace('    fun addObjective(objective: Objective) {\n        _state.update { it.copy(objectives = it.objectives + objective) }\n    }', add_method)

with open('app/src/main/java/com/example/MainViewModel.kt', 'w') as f:
    f.write(text)

