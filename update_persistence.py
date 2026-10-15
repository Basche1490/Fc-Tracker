import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

# Add imports
imports_to_add = """import android.content.Context
import android.content.SharedPreferences
import com.google.gson.reflect.TypeToken
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import androidx.lifecycle.viewModelScope
"""
if "android.content.SharedPreferences" not in content:
    content = content.replace("import com.google.gson.Gson", imports_to_add + "import com.google.gson.Gson")

# Remove existing init { }
content = re.sub(r'init \{\s*// Data initialized in completeOnboarding\s*\}', '', content)

persist_logic = """
    private val prefs: SharedPreferences = getApplication<android.app.Application>().getSharedPreferences("fc_manager_prefs", Context.MODE_PRIVATE)
    private val gson = Gson()

    init {
        loadPersistedData()
        viewModelScope.launch {
            while (true) {
                delay(2000)
                persistData()
            }
        }
    }

    private fun persistData() {
        saveSlots[activeSaveSlot] = _state.value
        if (!saveSlotNames.containsKey(activeSaveSlot)) {
            saveSlotNames[activeSaveSlot] = "Save Slot $activeSaveSlot (${_state.value.clubName})"
        }
        
        val slotsJson = gson.toJson(saveSlots)
        val namesJson = gson.toJson(saveSlotNames.toMap())
        val notesJson = gson.toJson(savedNotes.toList())
        
        prefs.edit()
            .putInt("activeSaveSlot", activeSaveSlot)
            .putString("saveSlots", slotsJson)
            .putString("saveSlotNames", namesJson)
            .putString("savedNotes", notesJson)
            .apply()
    }

    private fun loadPersistedData() {
        activeSaveSlot = prefs.getInt("activeSaveSlot", 1)
        
        val slotsJson = prefs.getString("saveSlots", null)
        if (slotsJson != null) {
            val type = object : TypeToken<Map<Int, AppState>>() {}.type
            try {
                val loadedSlots: Map<Int, AppState> = gson.fromJson(slotsJson, type)
                saveSlots.clear()
                saveSlots.putAll(loadedSlots)
            } catch (e: Exception) {}
        }
        
        val namesJson = prefs.getString("saveSlotNames", null)
        if (namesJson != null) {
            val type = object : TypeToken<Map<Int, String>>() {}.type
            try {
                val loadedNames: Map<Int, String> = gson.fromJson(namesJson, type)
                saveSlotNames.clear()
                saveSlotNames.putAll(loadedNames)
            } catch (e: Exception) {}
        }
        
        val notesJson = prefs.getString("savedNotes", null)
        if (notesJson != null) {
            val type = object : TypeToken<List<Note>>() {}.type
            try {
                val loadedNotes: List<Note> = gson.fromJson(notesJson, type)
                savedNotes.clear()
                savedNotes.addAll(loadedNotes)
            } catch (e: Exception) {}
        }
        
        if (saveSlots.containsKey(activeSaveSlot)) {
            _state.value = saveSlots[activeSaveSlot]!!
        }
    }
}"""

content = content.replace("    }\n}", "    }\n" + persist_logic)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
