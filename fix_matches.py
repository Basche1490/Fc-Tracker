import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

# Replace matchDate initialization to use state.startYear-08-01 if empty
text = text.replace('var matchDate by remember { mutableStateOf(initialMatch?.matchDate ?: "") }', 
'''var matchDate by remember { 
        mutableStateOf(initialMatch?.matchDate ?: run {
            val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
            val cal = java.util.Calendar.getInstance()
            cal.set(java.util.Calendar.YEAR, state.startYear)
            cal.set(java.util.Calendar.MONTH, java.util.Calendar.AUGUST)
            cal.set(java.util.Calendar.DAY_OF_MONTH, 1)
            sdf.format(cal.time)
        }) 
    }''')

# Add navigationBarsPadding to the MatchFormModal main column
text = text.replace('Column(modifier = Modifier.fillMaxSize().imePadding()) {', 'Column(modifier = Modifier.fillMaxSize().imePadding().navigationBarsPadding()) {')

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
