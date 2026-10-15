import re

def update_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # 1. Update the list of agents
    content = content.replace(
        'val aiAgents = listOf("Google Gemini - Free", "Grok - Free", "Claude Haiku - Free", "ChatGPT 3.5 - Free", "Paid Assistant Pro")',
        'val aiAgents = listOf("Google Gemini", "Grok", "Claude Haiku", "ChatGPT 3.5", "Other")'
    )
    
    # 2. Update the condition in OnboardingScreen.kt
    if "if (selectedAiAgent == \"Paid Assistant Pro\") {" in content:
        content = content.replace(
            "if (selectedAiAgent == \"Paid Assistant Pro\") {",
            "if (selectedAiAgent == \"Other\") {"
        )
        # Also need to make sure API key is always shown, except wait, the prompt asked:
        # "when a person selects any of the AI, it will ask for API key, and the former paid assistant to label as other and keep the API URL and API key field."
        # So for Other, show URL and Key. For others, show just Key.
        
        target_onboard = """                if (selectedAiAgent == "Other") {
                    OutlinedTextField(
                        value = aiApiUrl,
                        onValueChange = { aiApiUrl = it },
                        label = { Text("API URL") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                    OutlinedTextField(
                        value = aiApiKey,
                        onValueChange = { aiApiKey = it },
                        label = { Text("Pro API Key") },
                        modifier = Modifier.fillMaxWidth(),
                        visualTransformation = PasswordVisualTransformation(),
                        singleLine = true
                    )
                }"""
                
        replacement_onboard = """                if (selectedAiAgent == "Other") {
                    OutlinedTextField(
                        value = aiApiUrl,
                        onValueChange = { aiApiUrl = it },
                        label = { Text("API URL") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                }
                OutlinedTextField(
                    value = aiApiKey,
                    onValueChange = { aiApiKey = it },
                    label = { Text(if (selectedAiAgent == "Other") "API Key" else "${selectedAiAgent} API Key") },
                    modifier = Modifier.fillMaxWidth(),
                    visualTransformation = PasswordVisualTransformation(),
                    singleLine = true
                )"""
        content = content.replace(target_onboard, replacement_onboard)

    # 3. Update the condition in SettingsScreen.kt
    if "if (aiAgent == \"Paid Assistant Pro\") {" in content:
        content = content.replace(
            "if (aiAgent == \"Paid Assistant Pro\") {",
            "if (aiAgent == \"Other\") {"
        )
        
        target_settings = """                    if (aiAgent == "Other") {
                        OutlinedTextField(
                            value = aiApiUrl,
                            onValueChange = { aiApiUrl = it },
                            label = { Text("API URL") },
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                            singleLine = true
                        )
                        OutlinedTextField(
                            value = aiApiKey,
                            onValueChange = { aiApiKey = it },
                            label = { Text("Pro API Key") },
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                            visualTransformation = PasswordVisualTransformation(),
                            singleLine = true
                        )
                    }"""
                    
        replacement_settings = """                    if (aiAgent == "Other") {
                        OutlinedTextField(
                            value = aiApiUrl,
                            onValueChange = { aiApiUrl = it },
                            label = { Text("API URL") },
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                            singleLine = true
                        )
                    }
                    OutlinedTextField(
                        value = aiApiKey,
                        onValueChange = { aiApiKey = it },
                        label = { Text(if (aiAgent == "Other") "API Key" else "${aiAgent} API Key") },
                        modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                        visualTransformation = PasswordVisualTransformation(),
                        singleLine = true
                    )"""
        content = content.replace(target_settings, replacement_settings)

    with open(filepath, "w") as f:
        f.write(content)

update_file("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt")
update_file("app/src/main/java/com/example/ui/screens/SettingsScreen.kt")
