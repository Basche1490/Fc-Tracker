import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

text = text.replace('''var matchDate by remember { 
        mutableStateOf(initialMatch?.matchDate ?: run {
            val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
            val cal = java.util.Calendar.getInstance()
            cal.set(java.util.Calendar.YEAR, state.startYear)
            cal.set(java.util.Calendar.MONTH, java.util.Calendar.AUGUST)
            cal.set(java.util.Calendar.DAY_OF_MONTH, 1)
            sdf.format(cal.time)
        }) 
    }''', 'var matchDate by remember { mutableStateOf(initialMatch?.matchDate ?: "") }')

text = text.replace('label = { Text("Date (YYYY-MM-DD)") },', 'label = { Text("Date") },\n                                placeholder = { Text("YYYY-MM-DD") },')

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
