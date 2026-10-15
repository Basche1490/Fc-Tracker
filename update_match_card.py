import re

with open('app/src/main/java/com/example/ui/screens/MatchesScreen.kt', 'r') as f:
    text = f.read()

match_card = """@Composable
fun MatchCard(match: MatchResult, state: AppState? = null) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surfaceVariant)
            .padding(16.dp)
    ) {
        Column {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                Text(match.competition, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(match.matchDate, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                Text(if (match.isHome) "Home" else "Away", fontWeight = FontWeight.Bold, color = Color.White, modifier = Modifier.weight(1f))
                
                Box(modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(if (match.resultBadge == "W") WinColor else if (match.resultBadge == "D") DrawColor else LossColor).padding(horizontal = 8.dp, vertical = 4.dp)) {
                    Text("${match.goalsFor} - ${match.goalsAgainst}", color = Color.White, fontWeight = FontWeight.Bold)
                }
                
                Text(match.opponentName, fontWeight = FontWeight.Bold, color = Color.White, modifier = Modifier.weight(1f), textAlign = androidx.compose.ui.text.style.TextAlign.End)
            }
            
            val motm = match.playerPerformances.find { it.isMotm }
            if (motm != null && state != null) {
                Spacer(modifier = Modifier.height(8.dp))
                val player = state.players.find { it.id == motm.playerId }
                if (player != null) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(androidx.compose.material.icons.Icons.Default.Star, contentDescription = "MOTM", tint = Color.Yellow, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("MOTM: ${player.name}", fontSize = 12.sp, color = Color.White)
                    }
                }
            }
        }
    }
}
"""

text = re.sub(r'@Composable\nfun MatchCard\(match: MatchResult\) \{.*?\}\n\}\n', match_card, text, flags=re.DOTALL)
text = text.replace('MatchCard(match)', 'MatchCard(match, state)')

with open('app/src/main/java/com/example/ui/screens/MatchesScreen.kt', 'w') as f:
    f.write(text)
