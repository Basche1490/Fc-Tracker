import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_team_crest = r"""@Composable
fun TeamCrestImage\(teamName: String, modifier: Modifier = Modifier\) \{.*?
\}\n"""

new_team_crest = """@Composable
fun TeamCrestImage(teamName: String, modifier: Modifier = Modifier) {
    val url = getTeamCrestUrl(teamName)
    val fallbackBox = @Composable {
        Box(
            modifier = modifier.background(MaterialTheme.colorScheme.surfaceVariant),
            contentAlignment = Alignment.Center
        ) {
            val initials = teamName.split(" ").take(2).joinToString("") { it.take(1) }.uppercase()
            Text(if (initials.isNotEmpty()) initials else "?", color = Color.White, fontWeight = FontWeight.Bold)
        }
    }
    
    if (url.isNotEmpty()) {
        coil.compose.SubcomposeAsyncImage(
            model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                .data(url)
                .addHeader("User-Agent", "Mozilla/5.0")
                .crossfade(true)
                .build(),
            contentDescription = "$teamName Crest",
            contentScale = androidx.compose.ui.layout.ContentScale.Fit,
            modifier = modifier.background(Color.White),
            loading = { fallbackBox() },
            error = { fallbackBox() }
        )
    } else {
        fallbackBox()
    }
}
"""

content = re.sub(old_team_crest, new_team_crest, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
