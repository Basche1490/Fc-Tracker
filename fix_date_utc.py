import re
import glob

# Search across all UI screens
files = glob.glob("app/src/main/java/com/example/ui/screens/*.kt")

for file in files:
    with open(file, "r") as f:
        content = f.read()
    
    modified = False
    
    # SimpleDateFormat in TransfersScreen (transferDate init)
    if "java.text.SimpleDateFormat(\"yyyy-MM-dd\", java.util.Locale.getDefault()).format(java.util.Date())" in content:
        content = content.replace(
            "java.text.SimpleDateFormat(\"yyyy-MM-dd\", java.util.Locale.getDefault()).format(java.util.Date())",
            "java.text.SimpleDateFormat(\"yyyy-MM-dd\", java.util.Locale.getDefault()).apply { timeZone = java.util.TimeZone.getTimeZone(\"UTC\") }.format(java.util.Date())"
        )
        modified = True
    
    # Date picker logic where selectedDateMillis is used
    if "datePickerState.selectedDateMillis?.let { millis ->" in content:
        content = content.replace(
            "val sdf = java.text.SimpleDateFormat(\"yyyy-MM-dd\", java.util.Locale.getDefault())",
            "val sdf = java.text.SimpleDateFormat(\"yyyy-MM-dd\", java.util.Locale.getDefault()).apply { timeZone = java.util.TimeZone.getTimeZone(\"UTC\") }"
        )
        content = content.replace(
            "val sdf = SimpleDateFormat(\"yyyy-MM-dd\", Locale.getDefault())",
            "val sdf = SimpleDateFormat(\"yyyy-MM-dd\", Locale.getDefault()).apply { timeZone = java.util.TimeZone.getTimeZone(\"UTC\") }"
        )
        modified = True
        
    if modified:
        with open(file, "w") as f:
            f.write(content)
        print(f"Fixed UTC in {file}")

