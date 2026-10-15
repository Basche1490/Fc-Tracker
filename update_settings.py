with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    text = f.read()

import re

old_button = '''Button(onClick = { viewModel.updateSettings(clubName, managerName, leagueName, country, currencySymbol, primaryColorHex, secondaryColorHex, clubCrestUrl, aiAgent, aiApiUrl, aiApiKey) }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
                        Text("Save Profile Settings")
                    }'''

new_button = '''val context = androidx.compose.ui.platform.LocalContext.current
                    Button(onClick = { 
                        viewModel.updateSettings(clubName, managerName, leagueName, country, currencySymbol, primaryColorHex, secondaryColorHex, clubCrestUrl, aiAgent, aiApiUrl, aiApiKey)
                        android.widget.Toast.makeText(context, "Profile saved", android.widget.Toast.LENGTH_SHORT).show()
                    }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) {
                        Text("Save Profile Settings")
                    }'''

if old_button in text:
    text = text.replace(old_button, new_button)
else:
    print("Could not find button")

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(text)
