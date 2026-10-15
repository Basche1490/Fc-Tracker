with open('app/src/main/java/com/example/MainViewModel.kt', 'r') as f:
    text = f.read()

methods = """
    fun updateTransferBudget(budget: Double) {
        _uiState.update { it.copy(transferBudget = budget) }
    }

    fun addMatchResult(match: MatchResult) {
        _uiState.update { it.copy(recentMatches = it.recentMatches + match) }
    }
"""

text = text.replace('    fun updateObjective', methods + '\n    fun updateObjective')

with open('app/src/main/java/com/example/MainViewModel.kt', 'w') as f:
    f.write(text)

