import re
with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "r") as f:
    content = f.read()

data_class_addition = """
data class PlayerSeasonStats(val player: com.example.Player, var apps: Int = 0, var goals: Int = 0, var assists: Int = 0, var totalRating: Double = 0.0, var ratingCount: Int = 0) {
    val avgRating: Double get() = if (ratingCount > 0) totalRating / ratingCount else 0.0
}

@Composable
"""

content = content.replace("@Composable\nfun SquadStatsAwardsTab", data_class_addition + "fun SquadStatsAwardsTab")

old_squad_tab_start = r"fun SquadStatsAwardsTab\(state: AppState, onPlayerClick: \(com\.example\.Player\) -> Unit = \{\}, onShowAwards: \(\) -> Unit\) \{"
old_squad_tab_end = r"                \}\n            \}\n        \}\n    \}\n\}"

match = re.search(old_squad_tab_start + r".*?" + old_squad_tab_end, content, flags=re.DOTALL)
if match:
    old_squad_tab_full = match.group(0)

new_squad_tab = """fun SquadStatsAwardsTab(state: AppState, onPlayerClick: (com.example.Player) -> Unit = {}, onShowAwards: () -> Unit) {
    val seasonStatsMap = remember(state.recentMatches, state.players) {
        val map = mutableMapOf<String, PlayerSeasonStats>()
        state.players.forEach { map[it.id] = PlayerSeasonStats(it) }
        state.recentMatches.forEach { match ->
            match.playerPerformances.forEach { perf ->
                map[perf.playerId]?.let { s ->
                    s.apps++
                    s.goals += perf.goals
                    s.assists += perf.assists
                    s.totalRating += perf.rating
                    s.ratingCount++
                }
            }
        }
        map.values.toList().sortedByDescending { it.apps }
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item { OverviewStatsCard(state) }
        item {
            Button(onClick = onShowAwards, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)) {
                Text("Assign Awards & Honors")
            }
        }
        
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("Season Milestones & Record Holders", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(12.dp))
                
                val mostApps = seasonStatsMap.maxByOrNull { it.apps }
                val topScorer = seasonStatsMap.maxByOrNull { it.goals }
                val topAssists = seasonStatsMap.maxByOrNull { it.assists }
                val highestAvg = seasonStatsMap.filter { it.apps > 0 }.maxByOrNull { it.avgRating }
                
                RecordCardWithImage("Most Appearances", mostApps?.player?.displayName ?: "-", mostApps?.apps?.toString() ?: "0", mostApps?.player?.headshotUrl ?: "")
                Spacer(Modifier.height(8.dp))
                RecordCardWithImage("Top Scorer", topScorer?.player?.displayName ?: "-", topScorer?.goals?.toString() ?: "0", topScorer?.player?.headshotUrl ?: "")
                Spacer(Modifier.height(8.dp))
                RecordCardWithImage("Top Assists", topAssists?.player?.displayName ?: "-", topAssists?.assists?.toString() ?: "0", topAssists?.player?.headshotUrl ?: "")
            }
        }
        
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("Season Hall of Fame (Best Avg Rating)", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Name", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(2f))
                    Text("Apps", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                    Text("Avg", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                }
                Spacer(modifier = Modifier.height(4.dp))
                
                val topPlayers = seasonStatsMap.filter { it.apps >= 1 }.sortedByDescending { it.avgRating }.take(5)
                topPlayers.forEach { stat ->
                    Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(2f)) {
                            Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                                if (stat.player.headshotUrl.isNotEmpty()) {
                                    coil.compose.AsyncImage(
                                        model = stat.player.headshotUrl,
                                        contentDescription = stat.player.displayName,
                                        modifier = Modifier.fillMaxSize(),
                                        contentScale = androidx.compose.ui.layout.ContentScale.Crop
                                    )
                                } else {
                                    Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                                }
                            }
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("${stat.player.displayName}", color = Color.White, fontSize = 12.sp)
                        }
                        Text("${stat.apps}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text(String.format("%.1f", stat.avgRating), color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                    }
                    HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant)
                }
            }
        }
        
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("Season Player Statistics", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                
                Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Player", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(2f))
                    Text("Apps", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                    Text("Gls", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                    Text("Asts", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                }
                
                seasonStatsMap.forEach { stat ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { onPlayerClick(stat.player) }
                            .padding(vertical = 8.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("${stat.player.displayName}", color = Color.White, modifier = Modifier.weight(2f))
                        Text("${stat.apps}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text("${stat.goals}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text("${stat.assists}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                    }
                    HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant)
                }
            }
        }
    }
}

@Composable
fun RecordCardWithImage(title: String, playerName: String, recordValue: String, imageUrl: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(title, color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(modifier = Modifier.size(20.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                    if (imageUrl.isNotEmpty()) {
                        coil.compose.AsyncImage(
                            model = imageUrl,
                            contentDescription = playerName,
                            modifier = Modifier.fillMaxSize(),
                            contentScale = androidx.compose.ui.layout.ContentScale.Crop
                        )
                    } else {
                        Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(12.dp))
                    }
                }
                Spacer(modifier = Modifier.width(6.dp))
                Text(playerName, color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
        Text(recordValue, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
    }
}
"""

if match:
    content = content.replace(old_squad_tab_full, new_squad_tab)
    with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "w") as f:
        f.write(content)
else:
    print("NO MATCH for SquadStatsAwardsTab")
