import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

launcher_code = """
    val context = androidx.compose.ui.platform.LocalContext.current
    
    val exportLauncher = androidx.activity.compose.rememberLauncherForActivityResult(androidx.activity.result.contract.ActivityResultContracts.CreateDocument("application/octet-stream")) { uri ->
        uri?.let {
            try {
                val jsonStr = viewModel.exportStateToJson()
                val encryptedStr = com.example.utils.EncryptionUtils.encrypt(jsonStr)
                context.contentResolver.openOutputStream(it)?.use { out ->
                    out.write(encryptedStr.toByteArray())
                }
                android.widget.Toast.makeText(context, "Backup exported successfully", android.widget.Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                android.widget.Toast.makeText(context, "Failed to export", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
    }

    val importLauncher = androidx.activity.compose.rememberLauncherForActivityResult(androidx.activity.result.contract.ActivityResultContracts.GetContent()) { uri ->
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
    }

    Scaffold("""

content = content.replace("    Scaffold(", launcher_code)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
