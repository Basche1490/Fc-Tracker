import re

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

# 1. Update HeroBanner Dropdown
old_dropdown = """                    DropdownMenu(
                        expanded = seasonExpanded,
                        onDismissRequest = { seasonExpanded = false }
                    ) {"""

new_dropdown = """                    DropdownMenu(
                        expanded = seasonExpanded,
                        onDismissRequest = { seasonExpanded = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Start New Season") },
                            onClick = {
                                onSeasonSelected(-1) // Signals Start New Season
                                seasonExpanded = false
                            }
                        )"""

if 'text = { Text("Start New Season") }' not in content:
    content = content.replace(old_dropdown, new_dropdown)

old_nav = """HeroBanner(state, onMenuClick, { viewModel.setViewingSeasonYear(it) })"""
new_nav = """HeroBanner(state, onMenuClick, { 
                if (it == -1) viewModel.endSeason() else viewModel.setViewingSeasonYear(it) 
            })"""

content = content.replace(old_nav, new_nav)

# 2. Replace FinancialOverviewCard with LeaguePositionTrackerCard
# I'll replace the text in the actual code

old_fin = """fun FinancialOverviewCard(state: AppState) {
    val viewingSeason = state.historicalSeasons.find { it.year == state.viewingSeasonYear }
    val displayMatches = viewingSeason?.matches ?: state.recentMatches
    val displayPlayers = viewingSeason?.players ?: state.players

    DarkCard(modifier = Modifier.fillMaxWidth()) {
        Text("Financial Overview", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
        Spacer(modifier = Modifier.height(16.dp))
        
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Column {
                Text("Transfer Budget", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(state.currencySymbol + "${state.transferBudget}M", fontSize = 20.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.primary)
            }
            Column(horizontalAlignment = Alignment.End) {
                Text("Squad Value", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(state.currencySymbol + "${state.squadValue}M", fontSize = 20.sp, fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.secondary)
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Faux line graph for squad value projection
        Box(modifier = Modifier.fillMaxWidth().height(100.dp)) {
            Canvas(modifier = Modifier.fillMaxSize()) {
                val points = listOf(
                    androidx.compose.ui.geometry.Offset(0f, size.height * 0.8f),
                    androidx.compose.ui.geometry.Offset(size.width * 0.25f, size.height * 0.6f),
                    androidx.compose.ui.geometry.Offset(size.width * 0.5f, size.height * 0.7f),
                    androidx.compose.ui.geometry.Offset(size.width * 0.75f, size.height * 0.4f),
                    androidx.compose.ui.geometry.Offset(size.width, size.height * 0.2f)
                )
                
                val path = androidx.compose.ui.graphics.Path()
                points.forEachIndexed { index, point ->
                    if (index == 0) path.moveTo(point.x, point.y) else path.lineTo(point.x, point.y)
                }
                
                drawPath(
                    path = path,
                    color = androidx.compose.ui.graphics.Color(0xFF1E88E5), // primary
                    style = androidx.compose.ui.graphics.drawscope.Stroke(width = 3.dp.toPx())
                )
                
                // Draw dots
                points.forEach { point ->
                    drawCircle(
                        color = androidx.compose.ui.graphics.Color.White,
                        radius = 4.dp.toPx(),
                        center = point
                    )
                }
            }
        }
    }
}"""

new_fin = """fun FinancialOverviewCard(state: AppState) {
    val viewingSeason = state.historicalSeasons.find { it.year == state.viewingSeasonYear }
    val displayMatches = viewingSeason?.matches ?: state.recentMatches
    val leagueMatches = displayMatches.filter { it.competition == state.leagueName }.sortedBy { it.matchDate }

    DarkCard(modifier = Modifier.fillMaxWidth()) {
        Text("League Position Tracker", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
        Spacer(modifier = Modifier.height(16.dp))
        
        if (leagueMatches.isEmpty()) {
            Text("No league matches recorded yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        } else {
            val positions = leagueMatches.map { it.leaguePosition }
            val maxPos = (positions.maxOrNull() ?: 1).coerceAtLeast(20) // typically 1-20
            
            Box(modifier = Modifier.fillMaxWidth().height(120.dp)) {
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val stepX = if (positions.size > 1) size.width / (positions.size - 1).toFloat() else size.width
                    val path = androidx.compose.ui.graphics.Path()
                    
                    positions.forEachIndexed { index, pos ->
                        val y = if (maxPos > 1) ((pos - 1).toFloat() / (maxPos - 1).toFloat()) * size.height else 0f
                        val x = index * stepX
                        
                        if (index == 0) path.moveTo(x, y) else path.lineTo(x, y)
                    }
                    
                    drawPath(
                        path = path,
                        color = androidx.compose.ui.graphics.Color(0xFF1E88E5), // primary
                        style = androidx.compose.ui.graphics.drawscope.Stroke(width = 3.dp.toPx())
                    )
                    
                    positions.forEachIndexed { index, pos ->
                        val y = if (maxPos > 1) ((pos - 1).toFloat() / (maxPos - 1).toFloat()) * size.height else 0f
                        val x = index * stepX
                        drawCircle(
                            color = androidx.compose.ui.graphics.Color.White,
                            radius = 4.dp.toPx(),
                            center = androidx.compose.ui.geometry.Offset(x, y)
                        )
                    }
                }
            }
        }
    }
}"""

content = content.replace(old_fin, new_fin)

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)

