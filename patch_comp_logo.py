import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_comp_logo = r"""fun CompetitionLogoImage\(competition: String, modifier: Modifier = Modifier\) \{
    val initials = competition\.split\(" "\)\.take\(2\)\.joinToString\(""\) \{ it\.take\(1\) \}\.uppercase\(\)
    val bgColor = when \{
        competition\.contains\("Premier"\) -> Color\(0xFF38003C\)
        competition\.contains\("Champions"\) -> Color\(0xFF001489\)
        competition\.contains\("Europa"\) -> Color\(0xFFF68712\)
        competition\.contains\("La Liga"\) -> Color\(0xFFEE1222\)
        competition\.contains\("Serie A"\) -> Color\(0xFF0058A8\)
        competition\.contains\("Bundesliga"\) -> Color\(0xFFD20515\)
        else -> MaterialTheme\.colorScheme\.primary
    \}
    Box\(
        modifier = modifier\.background\(bgColor\),
        contentAlignment = Alignment\.Center
    \) \{
        Text\(initials, color = Color\.White, fontWeight = FontWeight\.Bold, fontSize = 12\.sp\)
    \}
\}"""

new_comp_logo = """fun getCompetitionLogoUrl(competition: String): String {
    val c = competition.lowercase()
    val domain = when {
        c.contains("premier") -> "premierleague.com"
        c.contains("champions") -> "uefa.com"
        c.contains("europa") -> "uefa.com"
        c.contains("la liga") -> "laliga.com"
        c.contains("serie a") -> "legaseriea.it"
        c.contains("bundesliga") -> "bundesliga.com"
        c.contains("ligue 1") -> "ligue1.com"
        c.contains("fa cup") -> "thefa.com"
        c.contains("carabao") || c.contains("efl") -> "efl.com"
        c.contains("world cup") -> "fifa.com"
        else -> return ""
    }
    return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${domain}&size=128"
}

@Composable
fun CompetitionLogoImage(competition: String, modifier: Modifier = Modifier) {
    val url = getCompetitionLogoUrl(competition)
    val fallbackBox = @Composable {
        val initials = competition.split(" ").take(2).joinToString("") { it.take(1) }.uppercase()
        val bgColor = when {
            competition.contains("Premier") -> Color(0xFF38003C)
            competition.contains("Champions") -> Color(0xFF001489)
            competition.contains("Europa") -> Color(0xFFF68712)
            competition.contains("La Liga") -> Color(0xFFEE1222)
            competition.contains("Serie A") -> Color(0xFF0058A8)
            competition.contains("Bundesliga") -> Color(0xFFD20515)
            else -> MaterialTheme.colorScheme.primary
        }
        Box(
            modifier = modifier.background(bgColor),
            contentAlignment = Alignment.Center
        ) {
            Text(initials, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)
        }
    }
    if (url.isNotEmpty()) {
        coil.compose.SubcomposeAsyncImage(
            model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                .data(url)
                .addHeader("User-Agent", "Mozilla/5.0")
                .crossfade(true)
                .build(),
            contentDescription = "$competition Logo",
            contentScale = androidx.compose.ui.layout.ContentScale.Fit,
            modifier = modifier,
            loading = { fallbackBox() },
            error = { fallbackBox() }
        )
    } else {
        fallbackBox()
    }
}"""

content = re.sub(old_comp_logo, new_comp_logo, content)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
