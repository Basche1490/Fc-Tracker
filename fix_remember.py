import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

# Replace remember { mutableStateOf(logToEdit?.<field> ?: <default>) }
# with remember(logToEdit) { mutableStateOf(logToEdit?.<field> ?: <default>) }

content = content.replace(
    "var transferType by remember { mutableStateOf(logToEdit?.type ?: \"In (Permanent)\") }",
    "var transferType by remember(logToEdit) { mutableStateOf(logToEdit?.type ?: \"In (Permanent)\") }"
)

content = content.replace(
    "var playerQuery by remember { mutableStateOf(logToEdit?.playerName ?: \"\") }",
    "var playerQuery by remember(logToEdit) { mutableStateOf(logToEdit?.playerName ?: \"\") }"
)

content = content.replace(
    "var includeSwap by remember { mutableStateOf(logToEdit?.includeSwap ?: false) }",
    "var includeSwap by remember(logToEdit) { mutableStateOf(logToEdit?.includeSwap ?: false) }"
)

content = content.replace(
    "var isRegen by remember { mutableStateOf(logToEdit?.isRegen ?: false) }",
    "var isRegen by remember(logToEdit) { mutableStateOf(logToEdit?.isRegen ?: false) }"
)

content = content.replace(
    "var teamQuery by remember { mutableStateOf(logToEdit?.fromToClub ?: \"\") }",
    "var teamQuery by remember(logToEdit) { mutableStateOf(logToEdit?.fromToClub ?: \"\") }"
)

content = content.replace(
    "var feeM by remember { mutableStateOf(logToEdit?.feeM?.toString() ?: \"\") }",
    "var feeM by remember(logToEdit) { mutableStateOf(logToEdit?.feeM?.toString() ?: \"\") }"
)

content = content.replace(
    "var transferDate by remember { mutableStateOf(if (logToEdit?.date?.isNotEmpty() == true) logToEdit.date else java.text.SimpleDateFormat(\"yyyy-MM-dd\", java.util.Locale.getDefault()).apply { timeZone = java.util.TimeZone.getTimeZone(\"UTC\") }.format(java.util.Date())) }",
    "var transferDate by remember(logToEdit) { mutableStateOf(if (logToEdit?.date?.isNotEmpty() == true) logToEdit.date else java.text.SimpleDateFormat(\"yyyy-MM-dd\", java.util.Locale.getDefault()).apply { timeZone = java.util.TimeZone.getTimeZone(\"UTC\") }.format(java.util.Date())) }"
)


with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(content)

