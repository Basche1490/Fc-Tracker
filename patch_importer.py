# Patch SettingsScreen.kt
with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    settings_code = f.read()

target_str = """    val importLauncher = androidx.activity.compose.rememberLauncherForActivityResult(androidx.activity.result.contract.ActivityResultContracts.GetContent()) { uri ->
        uri?.let {
            try {
                val encryptedStr = context.contentResolver.openInputStream(it)?.bufferedReader().use { reader -> reader?.readText() }
                if (encryptedStr != null) {
                    val jsonStr = com.example.utils.EncryptionUtils.decrypt(encryptedStr)
                    if (jsonStr.isNotEmpty()) {
                        val success = viewModel.importStateFromJson(jsonStr)
                        if (success) {
                            android.widget.Toast.makeText(context, "Backup imported successfully", android.widget.Toast.LENGTH_SHORT).show()
                        } else {
                            android.widget.Toast.makeText(context, "Failed to parse backup", android.widget.Toast.LENGTH_SHORT).show()
                        }
                    } else {
                        android.widget.Toast.makeText(context, "Invalid or corrupted backup file", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }
            } catch (e: Exception) {
                android.widget.Toast.makeText(context, "Failed to import", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
    }"""

replacement_str = """    val importLauncher = androidx.activity.compose.rememberLauncherForActivityResult(androidx.activity.result.contract.ActivityResultContracts.GetContent()) { uri ->
        uri?.let {
            try {
                val rawText = context.contentResolver.openInputStream(it)?.bufferedReader().use { reader -> reader?.readText() }
                if (rawText != null) {
                    val trimmed = rawText.trim()
                    val jsonStr = if (trimmed.startsWith("{") || trimmed.startsWith("[")) {
                        trimmed
                    } else {
                        val decrypted = com.example.utils.EncryptionUtils.decrypt(rawText)
                        if (decrypted.isNotEmpty()) decrypted else trimmed
                    }
                    val success = viewModel.importStateFromJson(jsonStr)
                    if (success) {
                        android.widget.Toast.makeText(context, "Career data imported successfully!", android.widget.Toast.LENGTH_SHORT).show()
                    } else {
                        android.widget.Toast.makeText(context, "Failed to parse career data JSON", android.widget.Toast.LENGTH_SHORT).show()
                    }
                }
            } catch (e: Exception) {
                android.widget.Toast.makeText(context, "Failed to import: ${e.message}", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
    }"""

if target_str in settings_code:
    settings_code = settings_code.replace(target_str, replacement_str)
    with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
        f.write(settings_code)
    print("SettingsScreen patched successfully!")
else:
    print("Target string not found in SettingsScreen, checking lines...")
    import re
    # Fallback regex replace
    pattern = r"val importLauncher = androidx\.activity\.compose\.rememberLauncherForActivityResult.*?android\.widget\.Toast\.makeText\(context, \"Failed to import\", android\.widget\.Toast\.LENGTH_SHORT\)\.show\(\)\s+\}\s+\}\s+\}"
    new_code, count = re.subn(pattern, replacement_str, settings_code, flags=re.DOTALL)
    if count > 0:
        with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
            f.write(new_code)
        print("SettingsScreen regex-patched successfully!")
    else:
        print("Could not patch SettingsScreen!")

# Patch MainViewModel.kt
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    vm_code = f.read()

vm_target = """    fun importStateFromJson(json: String): Boolean {
        return try {
            val importedState = Gson().fromJson(json, AppState::class.java)
            if (importedState != null) {
                _state.value = importedState
                true
            } else false
        } catch (e: Exception) {
            false
        }
    }"""

vm_replacement = """    fun importStateFromJson(json: String): Boolean {
        return try {
            val importedState = com.google.gson.Gson().fromJson(json, AppState::class.java)
            if (importedState != null) {
                val finalState = if (importedState.players.isNotEmpty() && !importedState.isOnboarded) {
                    importedState.copy(isOnboarded = true)
                } else {
                    importedState
                }
                _state.value = finalState
                true
            } else false
        } catch (e: Exception) {
            false
        }
    }"""

if vm_target in vm_code:
    vm_code = vm_code.replace(vm_target, vm_replacement)
    with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
        f.write(vm_code)
    print("MainViewModel patched successfully!")
else:
    print("vm_target not found directly, checking...")
