import re
with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "r") as f:
    content = f.read()

# 1. Update Hall of Fame icon
old_hof = """                                    Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                                        Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                                    }"""

new_hof = """                                    Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                                        if (player.headshotUrl.isNotEmpty()) {
                                            coil.compose.AsyncImage(
                                                model = player.headshotUrl,
                                                contentDescription = player.displayName,
                                                modifier = Modifier.fillMaxSize(),
                                                contentScale = androidx.compose.ui.layout.ContentScale.Crop
                                            )
                                        } else {
                                            Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                                        }
                                    }"""
content = content.replace(old_hof, new_hof)


# 2. Update Milestones to use RecordCardWithImage (which we'll just redefine locally to be safe, or just inline)
old_milestones = """                        val recordSigning = state.transfers.filter { it.type == "Transfer In" }.maxByOrNull { it.feeM }
                        val recordSale = state.transfers.filter { it.type == "Transfer Out" }.maxByOrNull { it.feeM }
                        
                        RecordCard("Most Appearances", mostApps?.displayName ?: "-", mostApps?.matchesPlayed?.toString() ?: "0")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("All-Time Top Scorer", topScorer?.displayName ?: "-", topScorer?.goals?.toString() ?: "0")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("All-Time Top Assists", topAssists?.displayName ?: "-", topAssists?.assists?.toString() ?: "0")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("Record Signing", recordSigning?.playerName ?: "-", state.currencySymbol + (recordSigning?.feeM?.toString() ?: "0") + "M")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("Record Sale", recordSale?.playerName ?: "-", state.currencySymbol + (recordSale?.feeM?.toString() ?: "0") + "M")"""

new_milestones = """                        val recordSigning = state.transfers.filter { it.type == "Transfer In" }.maxByOrNull { it.feeM }
                        val recordSale = state.transfers.filter { it.type == "Transfer Out" }.maxByOrNull { it.feeM }
                        
                        com.example.ui.screens.RecordCardWithImage("Most Appearances", mostApps?.displayName ?: "-", mostApps?.matchesPlayed?.toString() ?: "0", mostApps?.headshotUrl ?: "")
                        Spacer(Modifier.height(8.dp))
                        com.example.ui.screens.RecordCardWithImage("All-Time Top Scorer", topScorer?.displayName ?: "-", topScorer?.goals?.toString() ?: "0", topScorer?.headshotUrl ?: "")
                        Spacer(Modifier.height(8.dp))
                        com.example.ui.screens.RecordCardWithImage("All-Time Top Assists", topAssists?.displayName ?: "-", topAssists?.assists?.toString() ?: "0", topAssists?.headshotUrl ?: "")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("Record Signing", recordSigning?.playerName ?: "-", state.currencySymbol + (recordSigning?.feeM?.toString() ?: "0") + "M")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("Record Sale", recordSale?.playerName ?: "-", state.currencySymbol + (recordSale?.feeM?.toString() ?: "0") + "M")"""
content = content.replace(old_milestones, new_milestones)


# 3. Add Home vs Away Performance before "Hall of Fame"
# I'll inject it before "Hall of Fame" card
home_vs_away_card = """
                item {
                    val allMatches = state.historicalSeasons.flatMap { it.matches } + state.recentMatches
                    val homeMatches = allMatches.filter { it.isHome }
                    val awayMatches = allMatches.filter { !it.isHome }
                    
                    val homeWins = homeMatches.count { it.goalsFor > it.goalsAgainst }
                    val homeDraws = homeMatches.count { it.goalsFor == it.goalsAgainst }
                    val homeLosses = homeMatches.count { it.goalsFor < it.goalsAgainst }
                    val awayWins = awayMatches.count { it.goalsFor > it.goalsAgainst }
                    val awayDraws = awayMatches.count { it.goalsFor == it.goalsAgainst }
                    val awayLosses = awayMatches.count { it.goalsFor < it.goalsAgainst }

                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Text("All-Time Home vs Away Performance", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                        Spacer(Modifier.height(8.dp))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            DarkCard(modifier = Modifier.weight(1f)) {
                                Text("Home", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                                Text("W: $homeWins  D: $homeDraws  L: $homeLosses", color = Color.White, fontSize = 12.sp)
                                Text("GF: ${homeMatches.sumOf { it.goalsFor }}  GA: ${homeMatches.sumOf { it.goalsAgainst }}", color = Color.White, fontSize = 12.sp)
                            }
                            Spacer(Modifier.width(8.dp))
                            DarkCard(modifier = Modifier.weight(1f)) {
                                Text("Away", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                                Text("W: $awayWins  D: $awayDraws  L: $awayLosses", color = Color.White, fontSize = 12.sp)
                                Text("GF: ${awayMatches.sumOf { it.goalsFor }}  GA: ${awayMatches.sumOf { it.goalsAgainst }}", color = Color.White, fontSize = 12.sp)
                            }
                        }
                    }
                }
"""
old_hof_item_start = """                item {
                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Text("Hall of Fame (Best Players)", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)"""
content = content.replace(old_hof_item_start, home_vs_away_card + old_hof_item_start)


with open("app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt", "w") as f:
    f.write(content)

