with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

import re

old_func = """@Composable
fun getCompetitionLogoUrl(competition: String): String {
    val c = competition.lowercase()
    val domain = when {
        c.contains("premier") -> "premierleague.com"
        c.contains("champions") -> "uefa.com"
        c.contains("europa") -> "uefa.com"
        c.contains("la liga") -> "laliga.com"
        c.contains("serie a") -> "legaseriea.it"
        c.contains("bundesliga") -> "bundesliga.com"
        c.contains("ligue 1") -> "ligue1.com"
        c.contains("carabao") || c.contains("efl") -> "efl.com"
        c.contains("fa cup") -> "thefa.com"
        c.contains("world cup") -> "fifa.com"
        else -> return ""
    }
    return "https://icon.horse/icon/${domain}"
}"""

new_func = """@Composable
fun getCompetitionLogoUrl(competition: String): String {
    val c = competition.lowercase()
    
    if (c.contains("la liga")) return "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/LaLiga_logo_2023.svg/512px-LaLiga_logo_2023.svg.png"
    if (c.contains("segunda")) return "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/LaLiga_logo_2023.svg/512px-LaLiga_logo_2023.svg.png"
    if (c.contains("ligue 1")) return "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Ligue1.svg/512px-Ligue1.svg.png"
    if (c.contains("mls")) return "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/MLS_crest_logo_RGB_gradient.svg/512px-MLS_crest_logo_RGB_gradient.svg.png"

    val domain = when {
        c.contains("premier") -> "premierleague.com"
        c.contains("championship") || c.contains("league one") || c.contains("league two") || c.contains("carabao") || c.contains("efl") -> "efl.com"
        c.contains("champions") -> "uefa.com"
        c.contains("europa") || c.contains("conference") -> "uefa.com"
        c.contains("serie a") -> "legaseriea.it"
        c.contains("serie b") -> "legab.it"
        c.contains("bundesliga") -> "bundesliga.com"
        c.contains("fa cup") -> "thefa.com"
        c.contains("world cup") -> "fifa.com"
        c.contains("usl") -> "uslchampionship.com"
        else -> return ""
    }
    return "https://icon.horse/icon/${domain}"
}"""

if old_func in text:
    text = text.replace(old_func, new_func)
else:
    print("Could not find old func")

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
