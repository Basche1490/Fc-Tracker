import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# Make sure Date Picker uses UTC strictly for initialization
target_init_millis = """    val initialMillis = remember(state.startYear) {
        val cal = java.util.Calendar.getInstance()
        cal.set(java.util.Calendar.YEAR, state.startYear)
        cal.set(java.util.Calendar.MONTH, java.util.Calendar.AUGUST)
        cal.set(java.util.Calendar.DAY_OF_MONTH, 1)
        cal.timeInMillis
    }"""
new_init_millis = """    val initialMillis = remember(state.startYear) {
        val cal = java.util.Calendar.getInstance(java.util.TimeZone.getTimeZone("UTC"))
        cal.set(java.util.Calendar.YEAR, state.startYear)
        cal.set(java.util.Calendar.MONTH, java.util.Calendar.AUGUST)
        cal.set(java.util.Calendar.DAY_OF_MONTH, 1)
        cal.set(java.util.Calendar.HOUR_OF_DAY, 12)
        cal.set(java.util.Calendar.MINUTE, 0)
        cal.set(java.util.Calendar.SECOND, 0)
        cal.set(java.util.Calendar.MILLISECOND, 0)
        cal.timeInMillis
    }"""
content = content.replace(target_init_millis, new_init_millis)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
