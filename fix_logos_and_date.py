import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# Fix getTeamCrestUrl
old_crest = """fun getTeamCrestUrl(teamName: String): String {
    val exactMatch = clubDomains.entries.firstOrNull { it.key.equals(teamName, ignoreCase = true) }
    if (exactMatch != null) {
        return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${exactMatch.value}&size=512"
    }"""
new_crest = """fun getTeamCrestUrl(teamName: String): String {
    val exactMatch = clubDomains.entries.firstOrNull { it.key.equals(teamName, ignoreCase = true) }
    if (exactMatch != null) {
        return "https://icon.horse/icon/${exactMatch.value}"
    }"""
content = content.replace(old_crest, new_crest)

old_fuzzy_crest = """    return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${domain}&size=512\""""
new_fuzzy_crest = """    return "https://icon.horse/icon/${domain}\""""
content = content.replace(old_fuzzy_crest, new_fuzzy_crest)

# Fix getCompetitionLogoUrl
old_comp = """    val url = getCompetitionLogoUrl(competition)"""
old_comp_ret = """    return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${domain}&size=512\""""
new_comp_ret = """    return "https://icon.horse/icon/${domain}\""""
content = content.replace(old_comp_ret, new_comp_ret)

# Fix Avatar size for unknown teams
content = content.replace("size=256", "size=512")

# Fix Date Picker Alignment (ignore time, use UTC purely)
old_date = """                    datePickerState.selectedDateMillis?.let { millis ->
                        val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
                        sdf.timeZone = java.util.TimeZone.getTimeZone("UTC")
                        matchDate = sdf.format(java.util.Date(millis))
                    }"""
new_date = """                    datePickerState.selectedDateMillis?.let { millis ->
                        // Force UTC timezone to avoid shifting day
                        val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault())
                        sdf.timeZone = java.util.TimeZone.getTimeZone("UTC")
                        matchDate = sdf.format(java.util.Date(millis))
                    }"""
# Wait, I already fixed it to UTC! The user said: "For the date picker alignment, can you ignore the timestamp all together and just go by day?"
# Maybe I should just take the millis and construct the LocalDate properly in UTC, then print. Or maybe `initialMillis` is wrong.
old_initial_millis = """    val initialMillis = remember(state.startYear) {
        val cal = java.util.Calendar.getInstance()
        cal.set(java.util.Calendar.YEAR, state.startYear)
        cal.set(java.util.Calendar.MONTH, java.util.Calendar.AUGUST)
        cal.set(java.util.Calendar.DAY_OF_MONTH, 1)
        cal.timeInMillis
    }"""
new_initial_millis = """    val initialMillis = remember(state.startYear) {
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
content = content.replace(old_initial_millis, new_initial_millis)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

