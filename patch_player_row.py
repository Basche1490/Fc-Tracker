import re

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

old_row = r"""                    coil\.compose\.SubcomposeAsyncImage\(.*?\).*?\}"""
new_row = """                    coil.compose.SubcomposeAsyncImage(
                        model = player.headshotUrl,
                        contentDescription = "Player Headshot",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                        error = { Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.primary) }
                    )
                }
            }
            Spacer(Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(player.displayName, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.White)
                    if (player.isInjured) {
                        Spacer(Modifier.width(8.dp))
                        Icon(Icons.Default.Warning, contentDescription = "Injured", tint = Color.Red, modifier = Modifier.size(16.dp))
                    }
                    if (player.isLoanedOut) {
                        Spacer(Modifier.width(8.dp))
                        Box(modifier = Modifier.background(Color(0xFFF68712), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                            Text("Loaned Out", fontSize = 10.sp, color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    } else if (player.isLoanedIn) {
                        Spacer(Modifier.width(8.dp))
                        Box(modifier = Modifier.background(Color(0xFF0058A8), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                            Text("Loaned In", fontSize = 10.sp, color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }"""
content = re.sub(r"                    coil\.compose\.SubcomposeAsyncImage\(.*?\)\n                \}\n            \}\n            Spacer\(Modifier\.width\(16\.dp\)\)\n            Column\(modifier = Modifier\.weight\(1f\)\) \{\n                Text\(player\.displayName, fontWeight = FontWeight\.Bold, fontSize = 16\.sp, color = Color\.White\)", new_row, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)
