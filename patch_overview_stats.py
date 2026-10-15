import re
with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "r") as f:
    content = f.read()

old_func_start = r"fun OverviewStatsCard\(state: AppState\) \{"
old_func_end = r"                Text\(\"Wins: \$wins \| Draws: \$draws \| Losses: \$losses\", color = Color\.White\)\n            \}\n        \}\n    \}\n\}"

match = re.search(old_func_start + r".*?" + old_func_end, content, flags=re.DOTALL)
if match:
    old_func_full = match.group(0)

new_func = """fun OverviewStatsCard(state: AppState) {
    val leagueMatches = state.recentMatches.filter { it.competition == state.leagueName }
    val matchesPlayed = leagueMatches.size
    var wins = 0
    var draws = 0
    var losses = 0
    var goalsFor = 0
    var goalsAgainst = 0
    
    val homeMatches = leagueMatches.filter { it.isHome }
    val awayMatches = leagueMatches.filter { !it.isHome }
    val homeWins = homeMatches.count { it.goalsFor > it.goalsAgainst }
    val homeDraws = homeMatches.count { it.goalsFor == it.goalsAgainst }
    val homeLosses = homeMatches.count { it.goalsFor < it.goalsAgainst }
    val awayWins = awayMatches.count { it.goalsFor > it.goalsAgainst }
    val awayDraws = awayMatches.count { it.goalsFor == it.goalsAgainst }
    val awayLosses = awayMatches.count { it.goalsFor < it.goalsAgainst }
    
    leagueMatches.forEach { match ->
        goalsFor += match.goalsFor
        goalsAgainst += match.goalsAgainst
        when {
            match.goalsFor > match.goalsAgainst -> wins++
            match.goalsFor < match.goalsAgainst -> losses++
            else -> draws++
        }
    }
    val points = (wins * 3) + draws
    val goalDiff = goalsFor - goalsAgainst
    
    val position = leagueMatches.maxByOrNull { it.matchDate }?.leaguePosition ?: 1
    
    val last5 = state.recentMatches.sortedByDescending { it.matchDate }.take(5).reversed()
    
    DarkCard(modifier = Modifier.fillMaxWidth()) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            com.example.ui.screens.CompetitionLogoImage(competition = state.leagueName, modifier = Modifier.size(48.dp).clip(CircleShape))
            Spacer(Modifier.width(16.dp))
            Column {
                Text(state.leagueName, fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Text("Current Position: $position", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        Spacer(Modifier.height(16.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            StatBox("PTS", points.toString())
            StatBox("MP", matchesPlayed.toString())
            StatBox("GD", if (goalDiff > 0) "+$goalDiff" else goalDiff.toString())
        }
        
        Spacer(Modifier.height(16.dp))
        HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant)
        Spacer(Modifier.height(16.dp))
        
        Text("Form & Statistics", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
        Spacer(Modifier.height(8.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Last 5: ", color = MaterialTheme.colorScheme.onSurfaceVariant)
            last5.forEach { match ->
                val badgeColor = when {
                    match.goalsFor > match.goalsAgainst -> com.example.ui.theme.WinColor
                    match.goalsFor < match.goalsAgainst -> com.example.ui.theme.LossColor
                    else -> com.example.ui.theme.DrawColor
                }
                val badge = when {
                    match.goalsFor > match.goalsAgainst -> "W"
                    match.goalsFor < match.goalsAgainst -> "L"
                    else -> "D"
                }
                Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(badgeColor), contentAlignment = Alignment.Center) {
                    Text(badge, color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.width(4.dp))
            }
        }
        Spacer(Modifier.height(12.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Column {
                Text("Wins: $wins | Draws: $draws | Losses: $losses", color = Color.White)
                Row {
                    Text("Goals Scored: $goalsFor", color = Color.White)
                    Spacer(Modifier.width(16.dp))
                    Text("Goals Conceded: ${goalsAgainst.toString().toInt()}", color = Color.White)
                }
            }
        }
        
        Spacer(Modifier.height(16.dp))
        Text("Home vs Away Performance", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
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
}"""

if match:
    content = content.replace(old_func_full, new_func)
    with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "w") as f:
        f.write(content)
else:
    print("NO MATCH")
