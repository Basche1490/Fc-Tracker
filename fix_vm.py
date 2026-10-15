import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

bad_str = """    fun addMatchResult(match: MatchResult) {

    fun exportStateToJson(): String {
        return Gson().toJson(_state.value)
    }

    fun importStateFromJson(json: String): Boolean {
        return try {
            val importedState = Gson().fromJson(json, AppState::class.java)
            if (importedState != null) {
                _state.value = importedState
                true
            } else false
        } catch (e: Exception) {
            false
        }
    }
"""

good_str = """
    fun exportStateToJson(): String {
        return Gson().toJson(_state.value)
    }

    fun importStateFromJson(json: String): Boolean {
        return try {
            val importedState = Gson().fromJson(json, AppState::class.java)
            if (importedState != null) {
                _state.value = importedState
                true
            } else false
        } catch (e: Exception) {
            false
        }
    }

    fun addMatchResult(match: MatchResult) {"""

content = content.replace(bad_str, good_str)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
