import re

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "r") as f:
    content = f.read()

# Replace variables
content = content.replace("var filterSeasonYear by remember { mutableStateOf<Int?>(null) } // null = All-Time", "var filterSeasonYearHoF by remember { mutableStateOf<Int?>(null) }\n    var filterSeasonYearMilestones by remember { mutableStateOf<Int?>(null) }")
content = content.replace("var filterExpanded by remember { mutableStateOf(false) }", "var filterExpandedHoF by remember { mutableStateOf(false) }\n    var filterExpandedMilestones by remember { mutableStateOf(false) }")

# Replace displayStats
old_display_stats = """    val displayStats = remember(state.players, state.historicalSeasons, filterSeasonYear) {
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
    }"""

new_display_stats = """    val displayStatsHoF = remember(state.players, state.historicalSeasons, filterSeasonYearHoF) {
        if (filterSeasonYearHoF == null) {
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
        } else if (filterSeasonYearHoF == state.startYear) {
            state.players
        } else {
            state.historicalSeasons.find { it.year == filterSeasonYearHoF }?.players ?: emptyList()
        }
    }
    
    val displayStatsMilestones = remember(state.players, state.historicalSeasons, filterSeasonYearMilestones) {
        if (filterSeasonYearMilestones == null) {
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
        } else if (filterSeasonYearMilestones == state.startYear) {
            state.players
        } else {
            state.historicalSeasons.find { it.year == filterSeasonYearMilestones }?.players ?: emptyList()
        }
    }"""

content = content.replace(old_display_stats, new_display_stats)

# The standalone dropdown UI
old_dropdown_ui = """                                item {
                    Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.End) {
                        Box {
                            androidx.compose.material3.TextButton(onClick = { filterExpanded = true }) {
                                Text(if (filterSeasonYear == null) "All-Time" else if (filterSeasonYear == state.startYear) "${state.startYear}/${state.startYear+1} (Current)" else "${filterSeasonYear}/${filterSeasonYear!!+1}")
                                Text("▼", modifier = Modifier.padding(start=4.dp))
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
                }
                item {
                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Text("Hall of Fame (Best Players)", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)"""

new_hof_ui = """                item {
                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Hall of Fame (Best Players)", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            Box {
                                androidx.compose.material3.TextButton(onClick = { filterExpandedHoF = true }) {
                                    Text(if (filterSeasonYearHoF == null) "All-Time" else if (filterSeasonYearHoF == state.startYear) "${state.startYear}/${state.startYear+1} (Current)" else "${filterSeasonYearHoF}/${filterSeasonYearHoF!!+1}")
                                    Text("▼", modifier = Modifier.padding(start=4.dp))
                                }
                                DropdownMenu(expanded = filterExpandedHoF, onDismissRequest = { filterExpandedHoF = false }) {
                                    DropdownMenuItem(text = { Text("All-Time") }, onClick = { filterSeasonYearHoF = null; filterExpandedHoF = false })
                                    DropdownMenuItem(text = { Text("${state.startYear}/${state.startYear+1} (Current)") }, onClick = { filterSeasonYearHoF = state.startYear; filterExpandedHoF = false })
                                    state.historicalSeasons.forEach { s ->
                                        DropdownMenuItem(text = { Text("${s.year}/${s.year+1}") }, onClick = { filterSeasonYearHoF = s.year; filterExpandedHoF = false })
                                    }
                                }
                            }
                        }"""

content = content.replace(old_dropdown_ui, new_hof_ui)

content = content.replace("val topPlayers = displayStats.sortedWith", "val topPlayers = displayStatsHoF.sortedWith")

old_milestone_ui = """                item {
                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Text("Club Milestones & Record Holders", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                        Spacer(modifier = Modifier.height(12.dp))
                        
                        val mostApps = displayStats.maxByOrNull { it.matchesPlayed }
                        val topScorer = displayStats.maxByOrNull { it.goals }
                        val topAssists = displayStats.maxByOrNull { it.assists }
                        val highestAvg = displayStats.filter { it.matchesPlayed > 0 }.maxByOrNull { it.averageRating }"""

new_milestone_ui = """                item {
                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Club Milestones & Record Holders", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            Box {
                                androidx.compose.material3.TextButton(onClick = { filterExpandedMilestones = true }) {
                                    Text(if (filterSeasonYearMilestones == null) "All-Time" else if (filterSeasonYearMilestones == state.startYear) "${state.startYear}/${state.startYear+1} (Current)" else "${filterSeasonYearMilestones}/${filterSeasonYearMilestones!!+1}")
                                    Text("▼", modifier = Modifier.padding(start=4.dp))
                                }
                                DropdownMenu(expanded = filterExpandedMilestones, onDismissRequest = { filterExpandedMilestones = false }) {
                                    DropdownMenuItem(text = { Text("All-Time") }, onClick = { filterSeasonYearMilestones = null; filterExpandedMilestones = false })
                                    DropdownMenuItem(text = { Text("${state.startYear}/${state.startYear+1} (Current)") }, onClick = { filterSeasonYearMilestones = state.startYear; filterExpandedMilestones = false })
                                    state.historicalSeasons.forEach { s ->
                                        DropdownMenuItem(text = { Text("${s.year}/${s.year+1}") }, onClick = { filterSeasonYearMilestones = s.year; filterExpandedMilestones = false })
                                    }
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(12.dp))
                        
                        val mostApps = displayStatsMilestones.maxByOrNull { it.matchesPlayed }
                        val topScorer = displayStatsMilestones.maxByOrNull { it.goals }
                        val topAssists = displayStatsMilestones.maxByOrNull { it.assists }
                        val highestAvg = displayStatsMilestones.filter { it.matchesPlayed > 0 }.maxByOrNull { it.averageRating }"""

content = content.replace(old_milestone_ui, new_milestone_ui)

with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "w") as f:
    f.write(content)

