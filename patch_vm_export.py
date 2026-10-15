import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

import_str = """import java.util.UUID
import com.google.gson.Gson"""

content = content.replace("import java.util.UUID", import_str)

export_funcs = """    fun addMatchResult(match: MatchResult) {

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

content = content.replace("    fun addMatchResult(match: MatchResult) {", export_funcs)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
