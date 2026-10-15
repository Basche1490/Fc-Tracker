import re

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "r") as f:
    content = f.read()

# Replace FinancialOverviewCard with LeaguePositionTrackerCard
# I'll just rewrite it in python and replace the entire function

new_fin = """@Composable
fun FinancialOverviewCard(state: AppState) {
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
            val maxPos = (positions.maxOrNull() ?: 1).coerceAtLeast(20)
            
            var selectedDot by remember { mutableStateOf<Int?>(null) }
            
            Box(modifier = Modifier.fillMaxWidth().height(160.dp).pointerInput(Unit) {
                detectTapGestures { offset ->
                    val stepX = if (positions.size > 1) size.width / (positions.size - 1).toFloat() else size.width.toFloat()
                    val clickedIndex = (offset.x / stepX).roundToInt()
                    if (clickedIndex in positions.indices) {
                        val y = if (maxPos > 1) ((positions[clickedIndex] - 1).toFloat() / (maxPos - 1).toFloat()) * size.height else 0f
                        if (kotlin.math.abs(offset.y - y) < 40f) {
                            selectedDot = clickedIndex
                        } else {
                            selectedDot = null
                        }
                    } else {
                        selectedDot = null
                    }
                }
            }) {
                androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxSize()) {
                    val stepX = if (positions.size > 1) size.width / (positions.size - 1).toFloat() else size.width
                    val path = androidx.compose.ui.graphics.Path()
                    
                    positions.forEachIndexed { index, pos ->
                        val y = if (maxPos > 1) ((pos - 1).toFloat() / (maxPos - 1).toFloat()) * size.height else 0f
                        val x = index * stepX
                        
                        if (index == 0) path.moveTo(x, y) else path.lineTo(x, y)
                    }
                    
                    drawPath(
                        path = path,
                        color = WinColor,
                        style = androidx.compose.ui.graphics.drawscope.Stroke(width = 3.dp.toPx())
                    )
                    
                    positions.forEachIndexed { index, pos ->
                        val y = if (maxPos > 1) ((pos - 1).toFloat() / (maxPos - 1).toFloat()) * size.height else 0f
                        val x = index * stepX
                        drawCircle(
                            color = if (selectedDot == index) Color.White else WinColor,
                            radius = if (selectedDot == index) 6.dp.toPx() else 4.dp.toPx(),
                            center = androidx.compose.ui.geometry.Offset(x, y)
                        )
                    }
                }
                
                selectedDot?.let { index ->
                    val pos = positions[index]
                    val stepX = if (positions.size > 1) 1f / (positions.size - 1).toFloat() else 1f
                    val xFraction = index * stepX
                    
                    Box(modifier = Modifier.align(Alignment.TopStart).padding(top = 16.dp)) {
                        Text("MD ${index + 1}: Position $pos", color = Color.White, fontSize = 12.sp, modifier = Modifier.background(Color.Black.copy(alpha=0.7f), RoundedCornerShape(4.dp)).padding(4.dp))
                    }
                }
            }
        }
    }
}
"""

start_idx = content.find("@Composable\nfun FinancialOverviewCard")
end_idx = content.find("@Composable\nfun SquadSummaryStats")
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_fin + content[end_idx:]

with open("app/src/main/java/com/example/ui/screens/DashboardScreen.kt", "w") as f:
    f.write(content)

