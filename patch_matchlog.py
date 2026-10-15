import re

# 1. Update PlayerPerformance in MainViewModel
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
    "val passAccuracy: Int = 0,\n    val shotAccuracy: Int = 0,",
    "val passAccuracy: Int = 0,\n    val passes: Int = 0,\n    val shotAccuracy: Int = 0,\n    val shots: Int = 0,"
)

# 2. Add Save Slots logic to MainViewModel
save_slot_logic = """
    // Save Slot Logic
    var activeSaveSlot = 1
    val saveSlots = mutableMapOf<Int, AppState>()
    val saveSlotNames = mutableMapOf<Int, String>()
    
    fun switchSaveSlot(slot: Int, createNew: Boolean = false) {
        if (activeSaveSlot == slot) return
        
        // Save current to map
        saveSlots[activeSaveSlot] = _state.value
        if (!saveSlotNames.containsKey(activeSaveSlot)) {
            saveSlotNames[activeSaveSlot] = "Save Slot $activeSaveSlot (${_state.value.clubName})"
        }
        
        activeSaveSlot = slot
        if (createNew || !saveSlots.containsKey(slot)) {
            _state.value = AppState()
            saveSlotNames[slot] = "Save Slot $slot (New)"
        } else {
            _state.value = saveSlots[slot]!!
        }
    }
    
    fun deleteCurrentSave() {
        saveSlots.remove(activeSaveSlot)
        saveSlotNames.remove(activeSaveSlot)
        
        val nextSlot = saveSlots.keys.firstOrNull()
        if (nextSlot != null) {
            activeSaveSlot = nextSlot
            _state.value = saveSlots[nextSlot]!!
        } else {
            activeSaveSlot = 1
            _state.value = AppState()
        }
    }
    
    fun renameSaveSlot(slot: Int, name: String) {
        saveSlotNames[slot] = name
    }
"""

if "var activeSaveSlot" not in content:
    content = content.replace("fun exportStateToJson(): String {", save_slot_logic + "\n    fun exportStateToJson(): String {")

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)

