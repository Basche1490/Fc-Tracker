import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# 1. Update displayMatches logic
display_matches_logic = """    val displayMatches = if (state.viewingSeasonYear != null) {
        state.historicalSeasons.find { it.year == state.viewingSeasonYear }?.matches ?: emptyList()
    } else {
        state.recentMatches
    }
    val isArchived = state.viewingSeasonYear != null
"""
content = re.sub(r'(\s+)val df = SimpleDateFormat', r'\1' + display_matches_logic + r'\1val df = SimpleDateFormat', content)

# Replace state.recentMatches with displayMatches in the list view
content = content.replace("state.recentMatches.isNotEmpty()", "displayMatches.isNotEmpty()")
content = content.replace("state.recentMatches.first().matchDate", "displayMatches.first().matchDate")
content = content.replace("matches = state.recentMatches", "matches = displayMatches")
content = content.replace("state.recentMatches.map { it.competition }", "displayMatches.map { it.competition }")
content = content.replace("items(state.recentMatches.filter", "items(displayMatches.filter")
content = content.replace("if (state.recentMatches.filter", "if (displayMatches.filter")
content = content.replace("state.recentMatches.reversed().find", "displayMatches.reversed().find")

# Wrap FAB to not show if archived
fab_target = """        FloatingActionButton(
            onClick = { matchToEdit = null; showMatchForm = true },"""
fab_replacement = """        if (!isArchived) {
            FloatingActionButton(
                onClick = { matchToEdit = null; showMatchForm = true },"""
content = content.replace(fab_target, fab_replacement)
content = content.replace("""            Icon(Icons.Default.Add, "Log Match", tint = MaterialTheme.colorScheme.onPrimary)
        }
    }""", """            Icon(Icons.Default.Add, "Log Match", tint = MaterialTheme.colorScheme.onPrimary)
            }
        }
    }""")

# 2. Fix date picker timezone
date_picker_target = """                    datePickerState.selectedDateMillis?.let { millis ->
                        val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
                        matchDate = sdf.format(Date(millis))
                    }"""
date_picker_replacement = """                    datePickerState.selectedDateMillis?.let { millis ->
                        val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
                        sdf.timeZone = java.util.TimeZone.getTimeZone("UTC")
                        matchDate = sdf.format(Date(millis))
                    }"""
content = content.replace(date_picker_target, date_picker_replacement)

# 3. Increase crest resolution
crest_target = """return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${exactMatch.value}&size=128\""""
crest_replacement = """return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${exactMatch.value}&size=512\""""
content = content.replace(crest_target, crest_replacement)

# 4. Disable editing in MatchResultCard if archived
on_edit_target = """                        onEdit = { matchToEdit = match; showMatchForm = true },"""
on_edit_replacement = """                        onEdit = { if(!isArchived) { matchToEdit = match; showMatchForm = true } },"""
content = content.replace(on_edit_target, on_edit_replacement)

# Also disable delete if archived
on_delete_target = """                        onDelete = { viewModel.deleteMatchResult(match.id) }"""
on_delete_replacement = """                        onDelete = { if(!isArchived) viewModel.deleteMatchResult(match.id) }"""
content = content.replace(on_delete_target, on_delete_replacement)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

