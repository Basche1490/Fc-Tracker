import re

with open("app/src/main/java/com/example/ui/screens/DetailedPlayerStatsModal.kt", "r") as f:
    content = f.read()

# Signature update
content = content.replace("fun DetailedPlayerStatsModal(player: Player, showOvrGrowth: Boolean = false, onDismiss: () -> Unit) {", "fun DetailedPlayerStatsModal(state: com.example.AppState, player: Player, showOvrGrowth: Boolean = false, onDismiss: () -> Unit) {")

# Compute actual stats inside the composable
stats_logic = """    Dialog(onDismissRequest = onDismiss) {
        val allMatches = androidx.compose.runtime.remember(state.recentMatches, state.historicalSeasons) {
            (state.recentMatches + state.historicalSeasons.flatMap { it.matches }).sortedByDescending { it.matchDate }
        }
        val allPerformances = androidx.compose.runtime.remember(allMatches) {
            allMatches.mapNotNull { m -> (m.homePerformances + m.awayPerformances).find { it.playerId == player.id } }
        }
        val last5Ratings = allPerformances.take(5).map { it.rating }.reversed()
        val calcAvg = if (allPerformances.isNotEmpty()) allPerformances.map { it.rating }.average() else 0.0
        val starts = allPerformances.count { it.subInMinute == null }
        val subs = allPerformances.count { it.subInMinute != null }
        val startPct = if (starts + subs > 0) starts.toFloat() / (starts + subs) else 0f
        val cleanSheets = allPerformances.count { it.cleanSheet }
        val yellowCards = allPerformances.count { it.yellowCard }
        val redCards = allPerformances.count { it.redCard }
"""

content = content.replace("    Dialog(onDismissRequest = onDismiss) {", stats_logic)

# Form box replacement
form_box_old = """                            Text("Form (Last 5)", fontSize = 12.sp, color = Color.LightGray)
                            Spacer(Modifier.height(8.dp))
                            Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                // Mock 5 matches
                                listOf(8.2, 7.5, 6.0, 9.1, 7.8).forEach { rating ->
                                    val color = when {
                                        rating >= 8.0 -> Color.Green
                                        rating >= 7.0 -> Color.Yellow
                                        else -> Color.Red
                                    }
                                    Box(modifier = Modifier.size(20.dp).background(color, RoundedCornerShape(4.dp)), contentAlignment = Alignment.Center) {
                                        Text(rating.toString(), fontSize = 8.sp, color = Color.Black, fontWeight = FontWeight.Bold)
                                    }
                                }
                            }
                            Spacer(Modifier.height(8.dp))
                            Text("Avg: ${String.format("%.1f", player.averageRating)}", fontSize = 14.sp, color = Color.White, fontWeight = FontWeight.Bold)"""

form_box_new = """                            Text("Form (Last 5)", fontSize = 12.sp, color = Color.LightGray)
                            Spacer(Modifier.height(8.dp))
                            if (last5Ratings.isEmpty()) {
                                Text("No Data", fontSize = 12.sp, color = Color.Gray)
                            } else {
                                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                    last5Ratings.forEach { rating ->
                                        val color = when {
                                            rating >= 8.0 -> Color.Green
                                            rating >= 7.0 -> Color.Yellow
                                            else -> Color.Red
                                        }
                                        Box(modifier = Modifier.size(20.dp).background(color, RoundedCornerShape(4.dp)), contentAlignment = Alignment.Center) {
                                            Text(rating.toString(), fontSize = 8.sp, color = Color.Black, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                }
                            }
                            Spacer(Modifier.height(8.dp))
                            Text("Avg: ${String.format("%.1f", calcAvg)}", fontSize = 14.sp, color = Color.White, fontWeight = FontWeight.Bold)"""

content = content.replace(form_box_old, form_box_new)

# Usage box replacement
usage_box_old = """                            Text("Usage", fontSize = 12.sp, color = Color.LightGray)
                            val starts = player.matchesPlayed / 2 // Mock
                            val subs = player.matchesPlayed - starts
                            val startPct = if (player.matchesPlayed > 0) starts.toFloat() / player.matchesPlayed else 0f
                            
                            Text("Started: $starts", fontSize = 10.sp, color = Color.White)
                            LinearProgressIndicator(progress = { startPct }, modifier = Modifier.fillMaxWidth().height(4.dp).padding(vertical = 4.dp))
                            Text("Subbed: $subs", fontSize = 10.sp, color = Color.White)
                            LinearProgressIndicator(progress = { 1f - startPct }, modifier = Modifier.fillMaxWidth().height(4.dp).padding(vertical = 4.dp), color = Color.Cyan)"""

usage_box_new = """                            Text("Usage", fontSize = 12.sp, color = Color.LightGray)
                            Text("Started: $starts", fontSize = 10.sp, color = Color.White)
                            LinearProgressIndicator(progress = { startPct }, modifier = Modifier.fillMaxWidth().height(4.dp).padding(vertical = 4.dp))
                            Text("Subbed: $subs", fontSize = 10.sp, color = Color.White)
                            LinearProgressIndicator(progress = { if (starts + subs > 0) 1f - startPct else 0f }, modifier = Modifier.fillMaxWidth().height(4.dp).padding(vertical = 4.dp), color = Color.Cyan)"""

content = content.replace(usage_box_old, usage_box_new)

# Career stats mock replacements
stats_old = """                            StatRow("Clean Sheets", "0") // Mock
                            StatRow("Cards (Y/R)", "4Y / 1R") // Mock
                            StatRow("Avg Rating", String.format("%.1f", player.averageRating))"""

stats_new = """                            StatRow("Clean Sheets", cleanSheets.toString())
                            StatRow("Cards (Y/R)", "${yellowCards}Y / ${redCards}R")
                            StatRow("Avg Rating", String.format("%.1f", calcAvg))"""

content = content.replace(stats_old, stats_new)

# OVR Growth replacement
growth_old = """                                    val pts = listOf(player.startingOverall, player.startingOverall + 1, player.overall)
                                    val max = 99f
                                    val min = 40f
                                    val w = size.width / (pts.size - 1).coerceAtLeast(1)
                                    val path = androidx.compose.ui.graphics.Path()
                                    pts.forEachIndexed { i, pt ->
                                        val x = i * w
                                        val y = size.height - ((pt - min) / (max - min)) * size.height
                                        if (i == 0) path.moveTo(x, y) else path.lineTo(x, y)
                                        drawCircle(color = Color.Cyan, radius = 4f, center = Offset(x, y))
                                    }"""

growth_new = """                                    val earliestPlayer = state.historicalSeasons.sortedBy { it.year }.firstNotNullOfOrNull { s -> s.players.find { p -> p.id == player.id } }
                                    val initialOvr = earliestPlayer?.startingOverall ?: player.startingOverall
                                    val pts = listOf(initialOvr.toFloat(), player.startingOverall.toFloat())
                                    val max = 100f
                                    val min = 40f
                                    val w = size.width / (pts.size - 1).coerceAtLeast(1).toFloat()
                                    val path = androidx.compose.ui.graphics.Path()
                                    pts.forEachIndexed { i, pt ->
                                        val x = i * w
                                        val y = size.height - ((pt - min) / (max - min)) * size.height
                                        if (i == 0) path.moveTo(x, y) else path.lineTo(x, y)
                                        drawCircle(color = Color.Cyan, radius = 4f, center = androidx.compose.ui.geometry.Offset(x, y))
                                    }"""

content = content.replace(growth_old, growth_new)

with open("app/src/main/java/com/example/ui/screens/DetailedPlayerStatsModal.kt", "w") as f:
    f.write(content)

