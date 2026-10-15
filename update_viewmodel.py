import re

def add_update_players():
    with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
        content = f.read()

    target = """    fun updatePlayer(player: Player) {
        _state.update { current ->
            current.copy(players = current.players.map { if (it.id == player.id) player else it })
        }
    }"""
    
    replacement = """    fun updatePlayer(player: Player) {
        _state.update { current ->
            current.copy(players = current.players.map { if (it.id == player.id) player else it })
        }
    }

    fun updatePlayers(updatedPlayers: List<Player>) {
        _state.update { current ->
            val updatedMap = updatedPlayers.associateBy { it.id }
            current.copy(players = current.players.map { updatedMap[it.id] ?: it })
        }
    }"""
    
    content = content.replace(target, replacement)

    with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
        f.write(content)

add_update_players()
