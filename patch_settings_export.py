import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Add imports for context and URI and launcher
import_str = """import androidx.compose.ui.window.Dialog
import androidx.compose.ui.platform.LocalContext
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import android.widget.Toast
import com.example.utils.EncryptionUtils
"""

content = content.replace("import androidx.compose.ui.window.Dialog", import_str)

# Inside SettingsScreen, set up launchers
launcher_code = """    val aiAgents = listOf("Google Gemini - Free", "Grok - Free", "Claude Haiku - Free", "ChatGPT 3.5 - Free", "Paid Assistant Pro")
    
    val context = LocalContext.current
    
    val exportLauncher = rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("application/octet-stream")) { uri ->
        uri?.let {
            try {
                val jsonStr = viewModel.exportStateToJson()
                val encryptedStr = EncryptionUtils.encrypt(jsonStr)
                context.contentResolver.openOutputStream(it)?.use { out ->
                    out.write(encryptedStr.toByteArray())
                }
                Toast.makeText(context, "Backup exported successfully", Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                Toast.makeText(context, "Failed to export", Toast.LENGTH_SHORT).show()
            }
        }
    }

    val importLauncher = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        uri?.let {
            try {
                val encryptedStr = context.contentResolver.openInputStream(it)?.bufferedReader().use { reader -> reader?.readText() }
                if (encryptedStr != null) {
                    val jsonStr = EncryptionUtils.decrypt(encryptedStr)
                    if (jsonStr.isNotEmpty()) {
                        val success = viewModel.importStateFromJson(jsonStr)
                        if (success) {
                            Toast.makeText(context, "Backup imported successfully", Toast.LENGTH_SHORT).show()
                        } else {
                            Toast.makeText(context, "Failed to parse backup", Toast.LENGTH_SHORT).show()
                        }
                    } else {
                        Toast.makeText(context, "Invalid or corrupted backup file", Toast.LENGTH_SHORT).show()
                    }
                }
            } catch (e: Exception) {
                Toast.makeText(context, "Failed to import", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    Scaffold("""

content = content.replace("    val aiAgents = listOf(\"Google Gemini - Free\", \"Grok - Free\", \"Claude Haiku - Free\", \"ChatGPT 3.5 - Free\", \"Paid Assistant Pro\")\n    Scaffold(", launcher_code)

# Wire up the buttons
old_export_btn = r"                    Button\(onClick = \{ /\* Export \*/ \}, modifier = Modifier\.fillMaxWidth\(\)\) \{"
new_export_btn = """                    Button(onClick = { exportLauncher.launch("manager_backup.aes") }, modifier = Modifier.fillMaxWidth()) {"""
content = re.sub(old_export_btn, new_export_btn, content)

old_import_btn = r"                    Button\(onClick = \{ /\* Import JSON \*/ \}, modifier = Modifier\.fillMaxWidth\(\), colors = ButtonDefaults\.buttonColors\(containerColor = MaterialTheme\.colorScheme\.secondaryContainer\)\) \{"
new_import_btn = """                    Button(onClick = { importLauncher.launch("*/*") }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondaryContainer)) {"""
content = re.sub(old_import_btn, new_import_btn, content)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
