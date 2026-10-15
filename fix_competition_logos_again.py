import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

target = """fun getCompetitionLogoUrl(competition: String): String {
    val c = competition.lowercase()
    return when {
        c.contains("premier") -> "https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/1200px-Premier_League_Logo.svg.png"
        c.contains("champions") -> "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/UEFA_Champions_League_logo_2.svg/1200px-UEFA_Champions_League_logo_2.svg.png"
        c.contains("europa") -> "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Europa_League.svg/1200px-Europa_League.svg.png"
        c.contains("la liga") -> "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/LaLiga_logo_2023.svg/1200px-LaLiga_logo_2023.svg.png"
        c.contains("serie a") -> "https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/Serie_A_logo_%282022%29.svg/1200px-Serie_A_logo_%282022%29.svg.png"
        c.contains("bundesliga") -> "https://upload.wikimedia.org/wikipedia/en/thumb/d/df/Bundesliga_logo_%282017%29.svg/1200px-Bundesliga_logo_%282017%29.svg.png"
        c.contains("ligue 1") -> "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Ligue_1_McDonald%27s_2024.svg/1200px-Ligue_1_McDonald%27s_2024.svg.png"
        c.contains("carabao") || c.contains("efl") -> "https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/EFL_Cup.svg/1200px-EFL_Cup.svg.png"
        c.contains("fa cup") -> "https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Emirates_FA_Cup.svg/1200px-Emirates_FA_Cup.svg.png"
        c.contains("world cup") -> "https://upload.wikimedia.org/wikipedia/en/thumb/c/c5/FIFA_World_Cup_2026_Logo.svg/1200px-FIFA_World_Cup_2026_Logo.svg.png"
        else -> ""
    }
}"""

replacement = """fun getCompetitionLogoUrl(competition: String): String {
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

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
        f.write(content)
    print("Reverted to domain-based competition logos")
else:
    print("Could not find the target block")
