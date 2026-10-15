import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# 1. Add selectedCompetitionFilter
filter_state = """    var showMatchForm by remember { mutableStateOf(false) }
    var matchToEdit by remember { mutableStateOf<MatchResult?>(null) }
    var selectedCompetitionFilter by remember { mutableStateOf("All") }
"""
content = re.sub(r"    var showMatchForm by remember \{ mutableStateOf\(false\) \}\n    var matchToEdit by remember \{ mutableStateOf<MatchResult\?>\(null\) \}", filter_state, content)

# 2. Update Calendar Highlight colors and click behavior
# Look for FixtureCalendar parameters and day rendering.
fixture_cal_start = content.find("fun FixtureCalendar(")
fixture_cal_end = content.find("fun MatchResultCard(")

cal_code = content[fixture_cal_start:fixture_cal_end]
# Add onDateClick parameter
cal_code = cal_code.replace("matches: List<MatchResult>\n) {", "matches: List<MatchResult>,\n    onDateClick: (MatchResult) -> Unit\n) {")

# Update day box rendering
old_day_box = r"""Box\(\s*modifier = Modifier\s*\.weight\(1f\)\s*\.aspectRatio\(1f\)\s*\.padding\(2\.dp\)\s*\.clip\(CircleShape\)\s*\.background\(if \(dayMatches\.isNotEmpty\(\)\) MaterialTheme\.colorScheme\.primary else Color\.Transparent\),\s*contentAlignment = Alignment\.Center\s*\)"""
new_day_box = """val matchOnDay = dayMatches.firstOrNull()
                                val dayColor = if (matchOnDay != null) {
                                    when (matchOnDay.resultBadge) {
                                        "W" -> com.example.ui.theme.WinColor
                                        "D" -> com.example.ui.theme.DrawColor
                                        else -> com.example.ui.theme.LossColor
                                    }
                                } else { Color.Transparent }
                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .aspectRatio(1f)
                                        .padding(2.dp)
                                        .clip(CircleShape)
                                        .background(dayColor)
                                        .clickable(enabled = matchOnDay != null) {
                                            if (matchOnDay != null) onDateClick(matchOnDay)
                                        },
                                    contentAlignment = Alignment.Center
                                )"""
cal_code = re.sub(old_day_box, new_day_box, cal_code)
content = content[:fixture_cal_start] + cal_code + content[fixture_cal_end:]

# 3. Update FixtureCalendar usage inside MatchesScreen
usage_old = r"""FixtureCalendar\(\s*currentMonthCal = currentMonthCal,\s*onMonthChange = \{ newCal -> currentMonthCal = newCal \},\s*startCal = startCal,\s*endCal = endCal,\s*matches = state\.recentMatches\s*\)"""
usage_new = """FixtureCalendar(
                        currentMonthCal = currentMonthCal,
                        onMonthChange = { newCal -> currentMonthCal = newCal },
                        startCal = startCal,
                        endCal = endCal,
                        matches = state.recentMatches,
                        onDateClick = { m -> matchToEdit = m; showMatchForm = true }
                    )"""
content = re.sub(usage_old, usage_new, content)

# 4. Add Match History filter and apply it
history_title_old = r"""Text\("Match History", fontSize = 16\.sp, fontWeight = FontWeight\.Bold, color = Color\.White\)"""
history_title_new = """Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Text("Match History", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                        val allComps = listOf("All") + state.recentMatches.map { it.competition }.distinct().sorted()
                        var expanded by remember { mutableStateOf(false) }
                        Box {
                            TextButton(onClick = { expanded = true }) {
                                Text(selectedCompetitionFilter, color = MaterialTheme.colorScheme.primary)
                                Icon(Icons.Default.ArrowDropDown, contentDescription = "Filter", tint = MaterialTheme.colorScheme.primary)
                            }
                            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                                allComps.forEach { comp ->
                                    DropdownMenuItem(
                                        text = { Text(comp) },
                                        onClick = { selectedCompetitionFilter = comp; expanded = false }
                                    )
                                }
                            }
                        }
                    }"""
content = re.sub(history_title_old, history_title_new, content)

items_old = r"""items\(state\.recentMatches\) \{ match ->"""
items_new = """items(state.recentMatches.filter { selectedCompetitionFilter == "All" || it.competition == selectedCompetitionFilter }) { match ->"""
content = re.sub(items_old, items_new, content)

if_empty_old = r"""if \(state\.recentMatches\.isEmpty\(\)\) \{"""
if_empty_new = """if (state.recentMatches.filter { selectedCompetitionFilter == "All" || it.competition == selectedCompetitionFilter }.isEmpty()) {"""
content = re.sub(if_empty_old, if_empty_new, content)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
