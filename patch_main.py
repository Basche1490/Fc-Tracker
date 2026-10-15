import sys
with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

insert = """
        LaunchedEffect(drawerState.isOpen) {
            if (drawerState.isOpen) {
                focusManager.clearFocus()
            }
        }
        
        LaunchedEffect(Unit) {
            viewModel.startTelemetryPolling()
        }
        
        // Request Notification Permission on Android 13+
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            val launcher = androidx.activity.compose.rememberLauncherForActivityResult(
                androidx.activity.result.contract.ActivityResultContracts.RequestPermission()
            ) {}
            LaunchedEffect(Unit) {
                launcher.launch(android.Manifest.permission.POST_NOTIFICATIONS)
            }
        }
"""

content = content.replace("""        LaunchedEffect(drawerState.isOpen) {
            if (drawerState.isOpen) {
                focusManager.clearFocus()
            }
        }""", insert)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
