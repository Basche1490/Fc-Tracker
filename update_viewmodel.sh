sed -i '/fun updatePlayer(player: Player) {/i \
    fun addObjective(objective: Objective) {\
        _state.update { it.copy(objectives = it.objectives + objective) }\
    }\
\
    fun updateObjective(objective: Objective) {\
        _state.update { current ->\
            current.copy(objectives = current.objectives.map { if (it.id == objective.id) objective else it })\
        }\
    }\
\
    fun deleteObjective(id: String) {\
        _state.update { current ->\
            current.copy(objectives = current.objectives.filter { it.id != id })\
        }\
    }\
\
    fun addPlayer(player: Player) {\
        _state.update { it.copy(players = it.players + player) }\
    }\
\
    fun deletePlayer(id: String) {\
        _state.update { current ->\
            current.copy(players = current.players.filter { it.id != id })\
        }\
    }\
' app/src/main/java/com/example/MainViewModel.kt
