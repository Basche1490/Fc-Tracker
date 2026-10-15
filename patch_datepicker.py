import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_state = "val datePickerState = rememberDatePickerState()"

new_state = """val initialMillis = remember(state.startYear) {
        val cal = Calendar.getInstance()
        cal.set(Calendar.YEAR, state.startYear)
        cal.set(Calendar.MONTH, Calendar.AUGUST)
        cal.set(Calendar.DAY_OF_MONTH, 1)
        cal.timeInMillis
    }
    val datePickerState = rememberDatePickerState(initialSelectedDateMillis = if (matchDate.isEmpty()) initialMillis else null, initialDisplayedMonthMillis = if (matchDate.isEmpty()) initialMillis else null)"""

content = content.replace(old_state, new_state)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

