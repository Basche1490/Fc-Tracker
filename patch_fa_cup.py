import re
with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

old_func = """fun getCompetitionLogoUrl(competition: String): String {
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
}"""

new_func = """fun getCompetitionLogoUrl(competition: String): String {
    val c = competition.lowercase()
    if (c.contains("fa cup")) return "https://www.freelogovectors.net/wp-content/uploads/2022/01/facup-logo-freelogovectors.net_.png"
    val domain = when {
        c.contains("premier") -> "premierleague.com"
        c.contains("champions") -> "uefa.com"
        c.contains("europa") -> "uefa.com"
        c.contains("la liga") -> "laliga.com"
        c.contains("serie a") -> "legaseriea.it"
        c.contains("bundesliga") -> "bundesliga.com"
        c.contains("ligue 1") -> "ligue1.com"
        c.contains("carabao") || c.contains("efl") -> "efl.com"
        c.contains("world cup") -> "fifa.com"
        else -> return ""
    }
    return "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${domain}&size=128"
}"""

content = content.replace(old_func, new_func)
with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
