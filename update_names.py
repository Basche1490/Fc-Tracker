with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    text = f.read()

text = text.replace('"Save Slot $activeSaveSlot (${_state.value.clubName})"', '"Save Slot $activeSaveSlot"')
text = text.replace('"Save Slot $slot (New)"', '"Save Slot $slot"')

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(text)
