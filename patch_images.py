import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# 1. Add crest mapping function
if "fun getTeamCrestUrl(" not in content:
    crest_map = """
fun getTeamCrestUrl(teamName: String): String {
    val t = teamName.lowercase().replace(" ", "")
    return when {
        t.contains("arsenal") -> "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/120px-Arsenal_FC.svg.png"
        t.contains("astonvilla") -> "https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Aston_Villa_logo.svg/120px-Aston_Villa_logo.svg.png"
        t.contains("brentford") -> "https://upload.wikimedia.org/wikipedia/en/thumb/2/2a/Brentford_FC_crest.svg/120px-Brentford_FC_crest.svg.png"
        t.contains("brighton") -> "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/120px-Brighton_%26_Hove_Albion_logo.svg.png"
        t.contains("chelsea") -> "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/120px-Chelsea_FC.svg.png"
        t.contains("liverpool") -> "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/120px-Liverpool_FC.svg.png"
        t.contains("manchestercity") -> "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/120px-Manchester_City_FC_badge.svg.png"
        t.contains("manchesterunited") -> "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/120px-Manchester_United_FC_crest.svg.png"
        t.contains("newcastle") -> "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Newcastle_United_Logo.svg/120px-Newcastle_United_Logo.svg.png"
        t.contains("tottenham") -> "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/120px-Tottenham_Hotspur.svg.png"
        t.contains("realmadrid") -> "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/120px-Real_Madrid_CF.svg.png"
        t.contains("barcelona") -> "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/120px-FC_Barcelona_%28crest%29.svg.png"
        t.contains("atletico") -> "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Atletico_Madrid_2017_logo.svg/120px-Atletico_Madrid_2017_logo.svg.png"
        t.contains("bayern") -> "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/120px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png"
        t.contains("dortmund") -> "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Borussia_Dortmund_logo.svg/120px-Borussia_Dortmund_logo.svg.png"
        t.contains("juventus") -> "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Juventus_FC_2017_icon_%28black%29.svg/120px-Juventus_FC_2017_icon_%28black%29.svg.png"
        t.contains("acmilan") -> "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Logo_of_AC_Milan.svg/120px-Logo_of_AC_Milan.svg.png"
        t.contains("intermilan") -> "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/FC_Internazionale_Milano_2021.svg/120px-FC_Internazionale_Milano_2021.svg.png"
        t.contains("psg") || t.contains("paris") -> "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/120px-Paris_Saint-Germain_F.C..svg.png"
        else -> ""
    }
}
"""
    content += "\n" + crest_map

# 2. Add Team Logo & Competition Logo Composables
if "@Composable\nfun TeamCrestImage(" not in content:
    composables = """
@Composable
fun TeamCrestImage(teamName: String, modifier: Modifier = Modifier) {
    val url = getTeamCrestUrl(teamName)
    if (url.isNotEmpty()) {
        coil.compose.AsyncImage(
            model = url,
            contentDescription = "$teamName Crest",
            contentScale = androidx.compose.ui.layout.ContentScale.Fit,
            modifier = modifier.background(Color.White)
        )
    } else {
        Box(
            modifier = modifier.background(MaterialTheme.colorScheme.surfaceVariant),
            contentAlignment = Alignment.Center
        ) {
            val initials = teamName.split(" ").take(2).joinToString("") { it.take(1) }.uppercase()
            Text(if (initials.isNotEmpty()) initials else "?", color = Color.White, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun CompetitionLogoImage(competition: String, modifier: Modifier = Modifier) {
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
"""
    content += "\n" + composables

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
