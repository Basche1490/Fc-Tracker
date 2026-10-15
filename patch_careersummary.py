import re

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "r") as f:
    content = f.read()

# Add imports if missing
imports = """
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
"""
if "import androidx.compose.material3.DropdownMenu" not in content:
    content = content.replace("import androidx.compose.runtime.remember", "import androidx.compose.runtime.remember\n" + imports)

# Setup filter and sorting logic
logic_to_insert = """    var filterSeasonYear by remember { mutableStateOf<Int?>(null) } // null = All-Time
    var filterExpanded by remember { mutableStateOf(false) }
    
    var sortMode by remember { mutableStateOf("Rating") } // "Name", "Apps", "Goals", "Assists", "Rating"

    val displayStats = remember(state.players, state.historicalSeasons, filterSeasonYear) {
        if (filterSeasonYear == null) {
            val map = mutableMapOf<String, com.example.Player>()
            state.players.forEach { map[it.id] = it.copy() }
            state.historicalSeasons.forEach { season ->
                season.players.forEach { hp ->
                    val current = map[hp.id]
                    if (current != null) {
                        map[hp.id] = current.copy(
                            matchesPlayed = current.matchesPlayed + hp.matchesPlayed,
                            goals = current.goals + hp.goals,
                            assists = current.assists + hp.assists,
                            averageRating = if (current.averageRating == 0.0) hp.averageRating else if (hp.averageRating == 0.0) current.averageRating else (current.averageRating + hp.averageRating) / 2
                        )
                    } else {
                        map[hp.id] = hp.copy()
                    }
                }
            }
            map.values.toList()
        } else if (filterSeasonYear == state.startYear) {
            state.players
        } else {
            state.historicalSeasons.find { it.year == filterSeasonYear }?.players ?: emptyList()
        }
    }
"""

content = content.replace("    val allTimeStats = remember(state.players, state.historicalSeasons) {", logic_to_insert + "    val allTimeStats = remember(state.players, state.historicalSeasons) {")

# Replace allTimeStats with displayStats in the relevant parts, but keep allTimeStats for All-Time Squad List? The prompt says "Make a toggle for both Hall of fame and club milestone". All-Time Squad list could also use it, but let's change all.
content = content.replace("allTimeStats.sortedByDescending { it.averageRating }.take(5)", "displayStats.sortedWith(compareByDescending<com.example.Player> { when(sortMode) { \"Apps\" -> it.matchesPlayed.toDouble(); \"Goals\" -> it.goals.toDouble(); \"Assists\" -> it.assists.toDouble(); \"Name\" -> -it.displayName.hashCode().toDouble(); else -> it.averageRating } }).take(5)")
content = content.replace("val topPlayers = displayStats.sortedByDescending", "val topPlayers = displayStats.sortedByDescending") # if already matched

# Also need to replace allTimeStats with displayStats everywhere else
content = content.replace("allTimeStats.maxByOrNull", "displayStats.maxByOrNull")
content = content.replace("allTimeStats.filter", "displayStats.filter")
content = content.replace("allTimeStats.forEach", "displayStats.forEach")

# Replace sorting headers in Hall of Fame
old_headers = """                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Name", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(2f))
                            Text("Apps", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                            Text("Gls", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                            Text("Ast", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                        }"""

new_headers = """                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Name" + if(sortMode=="Name") "↓" else "", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(2f).clickable { sortMode = "Name" })
                            Text("Apps" + if(sortMode=="Apps") "↓" else "", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f).clickable { sortMode = "Apps" })
                            Text("Gls" + if(sortMode=="Goals") "↓" else "", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f).clickable { sortMode = "Goals" })
                            Text("Ast" + if(sortMode=="Assists") "↓" else "", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f).clickable { sortMode = "Assists" })
                        }"""

content = content.replace(old_headers, new_headers)

# Add dropdown before Hall of Fame
dropdown_ui = """                item {
                    Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.End) {
                        Box {
                            androidx.compose.material3.TextButton(onClick = { filterExpanded = true }) {
                                Text(if (filterSeasonYear == null) "All-Time" else if (filterSeasonYear == state.startYear) "${state.startYear}/${state.startYear+1} (Current)" else "${filterSeasonYear}/${filterSeasonYear!!+1}")
                                Icon(androidx.compose.material.icons.Icons.Default.ArrowDropDown, "")
                            }
                            DropdownMenu(expanded = filterExpanded, onDismissRequest = { filterExpanded = false }) {
                                DropdownMenuItem(text = { Text("All-Time") }, onClick = { filterSeasonYear = null; filterExpanded = false })
                                DropdownMenuItem(text = { Text("${state.startYear}/${state.startYear+1} (Current)") }, onClick = { filterSeasonYear = state.startYear; filterExpanded = false })
                                state.historicalSeasons.forEach { s ->
                                    DropdownMenuItem(text = { Text("${s.year}/${s.year+1}") }, onClick = { filterSeasonYear = s.year; filterExpanded = false })
                                }
                            }
                        }
                    }
                }"""

content = content.replace("item {\n                    DarkCard(modifier = Modifier.fillMaxWidth()) {\n                        Text(\"Hall of Fame (Best Players)\"", dropdown_ui + "\n                item {\n                    DarkCard(modifier = Modifier.fillMaxWidth()) {\n                        Text(\"Hall of Fame (Best Players)\"")

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "w") as f:
    f.write(content)
