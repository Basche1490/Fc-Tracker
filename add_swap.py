import re
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

swap_func = """    fun swapPlayers(id1: String, id2: String) {
        _state.update { current ->
            val list = current.players.toMutableList()
            val idx1 = list.indexOfFirst { it.id == id1 }
            val idx2 = list.indexOfFirst { it.id == id2 }
            if (idx1 != -1 && idx2 != -1) {
                val temp = list[idx1]
                list[idx1] = list[idx2]
                list[idx2] = temp
            }
            current.copy(players = list)
        }
    }
"""

content = content.replace("fun updatePlayers(updatedPlayers: List<Player>) {", swap_func + "\n    fun updatePlayers(updatedPlayers: List<Player>) {")

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
