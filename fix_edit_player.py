import re
with open("app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt", "r") as f:
    content = f.read()

# Add var status
if "var status by remember" not in content:
    content = content.replace(
        "var headshotUrl by remember { mutableStateOf(player?.headshotUrl ?: \"\") }",
        "var headshotUrl by remember { mutableStateOf(player?.headshotUrl ?: \"\") }\n    var status by remember { mutableStateOf(player?.status ?: \"Active\") }"
    )

# Add Dropdown for Status
if "DropdownField(\"Status\"" not in content:
    content = content.replace(
        "DropdownField(\"Tertiary Position\", tertiaryPosition, positions) { tertiaryPosition = it }",
        'DropdownField("Tertiary Position", tertiaryPosition, positions) { tertiaryPosition = it }\n                DropdownField("Status", status, listOf("Active", "Sold", "Loaned Out", "Loaned In", "Injured", "Academy")) { status = it }'
    )

# Add status to Player constructor
content = content.replace(
    "isRegen = isRegen",
    "isRegen = isRegen,\n                                status = status"
)

with open("app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt", "w") as f:
    f.write(content)
