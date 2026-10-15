import re
with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_card = """                    Column {
                        Text("vs ${match.opponentName}", fontWeight = FontWeight.Bold, color = Color.White, fontSize = 16.sp)
                        Text("${match.competition} • ${match.matchDate}", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("${match.goalsFor} - ${match.goalsAgainst}", fontSize = 20.sp, fontWeight = FontWeight.Black, color = badgeColor)
                    Spacer(Modifier.width(8.dp))
                    IconButton(onClick = onDelete, modifier = Modifier.size(24.dp)) {
                        Icon(Icons.Default.Delete, "Delete", tint = MaterialTheme.colorScheme.error)
                    }
                }"""

new_card = """                    Column {
                        val homeAwayStr = if (match.isHome) "(H)" else "(A)"
                        Text("$homeAwayStr vs ${match.opponentName}", fontWeight = FontWeight.Bold, color = Color.White, fontSize = 16.sp)
                        Text("${match.competition} • ${match.matchDate}", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Column(horizontalAlignment = Alignment.End) {
                        Text("${match.goalsFor} - ${match.goalsAgainst}", fontSize = 20.sp, fontWeight = FontWeight.Black, color = badgeColor)
                        if (match.homePenalties > 0 || match.awayPenalties > 0) {
                            Text("(${match.homePenalties} - ${match.awayPenalties} pens)", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                    Spacer(Modifier.width(8.dp))
                    IconButton(onClick = onDelete, modifier = Modifier.size(24.dp)) {
                        Icon(Icons.Default.Delete, "Delete", tint = MaterialTheme.colorScheme.error)
                    }
                }"""

content = content.replace(old_card, new_card)
with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
