import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# I need to find `fun getTeamCrestUrl` and replace it entirely to use the Google Favicon API.
old_get_crest = r"""fun getTeamCrestUrl\(teamName: String\): String \{
    val t = teamName\.lowercase\(\)\.replace\(" ", ""\)
    return when \{
        t\.contains\("arsenal"\) -> "https://upload\.wikimedia\.org/wikipedia/en/thumb/5/53/Arsenal_FC\.svg/120px-Arsenal_FC\.svg\.png"
.*?
    \}
\}"""

# In the MatchesScreen I want to replace `getTeamCrestUrl` logic, or better yet, inject the map.
new_get_crest = """val clubDomains = mapOf(
    "Arsenal" to "arsenal.com",
    "Aston Villa" to "avfc.co.uk",
    "Chelsea" to "chelseafc.com",
    "Everton" to "evertonfc.com",
    "Liverpool" to "liverpoolfc.com",
    "Manchester City" to "mancity.com",
    "Manchester United" to "manutd.com",
    "Newcastle United" to "nufc.co.uk",
    "Tottenham Hotspur" to "tottenhamhotspur.com",
    "Real Madrid" to "realmadrid.com",
    "Barcelona" to "fcbarcelona.com",
    "Atletico Madrid" to "atleticodemadrid.com",
    "Bayern Munich" to "fcbayern.com",
    "Borussia Dortmund" to "bvb.de",
    "Bayer Leverkusen" to "bayer04.de",
    "Juventus" to "juventus.com",
    "AC Milan" to "acmilan.com",
    "Inter Milan" to "inter.it",
    "Napoli" to "sscnapoli.it",
    "Roma" to "asroma.com",
    "Paris Saint-Germain" to "psg.fr",
    "Marseille" to "om.fr",
    "Lyon" to "ol.fr",
    "Ajax" to "ajax.nl",
    "PSV" to "psv.nl",
    "Feyenoord" to "feyenoord.nl",
    "Benfica" to "slbenfica.pt",
    "Porto" to "fcporto.pt",
    "Sporting CP" to "sporting.pt",
    "Al Nassr" to "alnassr.sa",
    "Al Hilal" to "alhilal.com",
    "Al Ittihad" to "ittihadclub.sa",
    "Inter Miami" to "intermiamicf.com",
    "LA Galaxy" to "lagalaxy.com"
)

fun getTeamCrestUrl(teamName: String): String {
    val exactMatch = clubDomains.entries.firstOrNull { it.key.equals(teamName, ignoreCase = true) }
    if (exactMatch != null) {
        return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${exactMatch.value}&size=128"
    }
    
    // Fuzzy matching for typed names
    val t = teamName.lowercase().replace(" ", "")
    val domain = when {
        t.contains("arsenal") -> "arsenal.com"
        t.contains("astonvilla") -> "avfc.co.uk"
        t.contains("brentford") -> "brentfordfc.com"
        t.contains("brighton") -> "brightonandhovealbion.com"
        t.contains("chelsea") -> "chelseafc.com"
        t.contains("liverpool") -> "liverpoolfc.com"
        t.contains("manchestercity") -> "mancity.com"
        t.contains("manchesterunited") -> "manutd.com"
        t.contains("newcastle") -> "nufc.co.uk"
        t.contains("tottenham") -> "tottenhamhotspur.com"
        t.contains("realmadrid") -> "realmadrid.com"
        t.contains("barcelona") -> "fcbarcelona.com"
        t.contains("atletico") -> "atleticodemadrid.com"
        t.contains("bayern") -> "fcbayern.com"
        t.contains("dortmund") -> "bvb.de"
        t.contains("juventus") -> "juventus.com"
        t.contains("acmilan") -> "acmilan.com"
        t.contains("intermilan") || t.contains("inter") -> "inter.it"
        t.contains("psg") || t.contains("paris") -> "psg.fr"
        t.contains("ajax") -> "ajax.nl"
        else -> return ""
    }
    return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${domain}&size=128"
}"""

content = re.sub(old_get_crest, new_get_crest, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
