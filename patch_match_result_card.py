import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_card = r"""                    TeamCrestImage\(teamName = match\.opponentName, modifier = Modifier\.size\(32\.dp\)\.clip\(CircleShape\)\)
                    Spacer\(Modifier\.width\(8\.dp\)\)
                    Box\(
                        modifier = Modifier\.size\(32\.dp\)\.clip\(CircleShape\)\.background\(badgeColor\),
                        contentAlignment = Alignment\.Center
                    \) \{
                        Text\(match\.resultBadge, color = Color\.White, fontWeight = FontWeight\.Bold\)
                    \}
                    Spacer\(Modifier\.width\(12\.dp\)\)
                    Column \{
                        Text\("vs \$\{match\.opponentName\}", fontWeight = FontWeight\.Bold, color = Color\.White, fontSize = 16\.sp\)
                        Text\("\$\{match\.competition\} • \$\{match\.matchDate\}", fontSize = 10\.sp, color = MaterialTheme\.colorScheme\.onSurfaceVariant\)
                    \}
                \}
                Row\(verticalAlignment = Alignment\.CenterVertically\) \{
                    Text\("\$\{match\.goalsFor\} - \$\{match\.goalsAgainst\}", fontSize = 20\.sp, fontWeight = FontWeight\.Black, color = Color\.White\)"""

new_card = """                    TeamCrestImage(teamName = match.opponentName, modifier = Modifier.size(32.dp).clip(CircleShape))
                    Spacer(Modifier.width(12.dp))
                    Column {
                        Text("vs ${match.opponentName}", fontWeight = FontWeight.Bold, color = Color.White, fontSize = 16.sp)
                        Text("${match.competition} • ${match.matchDate}", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("${match.goalsFor} - ${match.goalsAgainst}", fontSize = 20.sp, fontWeight = FontWeight.Black, color = badgeColor)"""

content = re.sub(old_card, new_card, content)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
