import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

leagues_map = """    val leaguesByCountry = mapOf(
        "England" to listOf("Premier League", "Championship", "League One", "League Two"),
        "Italy" to listOf("Serie A", "Serie B"),
        "France" to listOf("Ligue 1", "Ligue 2"),
        "Germany" to listOf("Bundesliga", "2. Bundesliga", "3. Liga"),
        "Spain" to listOf("La Liga", "Segunda División"),
        "Saudi" to listOf("Roshn Saudi League"),
        "America" to listOf("MLS", "USL Championship"),
        "USA" to listOf("MLS", "USL Championship"),
        "Brazil" to listOf("Brasileirão Série A", "Série B"),
        "Argentina" to listOf("Primera División"),
        "Portugal" to listOf("Liga Portugal"),
        "Netherlands" to listOf("Eredivisie")
    )
"""

if "leaguesByCountry" not in content:
    content = content.replace("fun SettingsScreen(", leagues_map + "\n@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SettingsScreen(")


# Now let's update the leagues dropdown
old_leagues_list = """                            val leagues = listOf("Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "MLS", "Other")
                            leagues.forEach { selectionOption ->"""

new_leagues_list = """                            val leagues = leaguesByCountry[country] ?: listOf("Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "MLS", "Other")
                            leagues.forEach { selectionOption ->"""

content = content.replace(old_leagues_list, new_leagues_list)

# And in OnboardingScreen.kt
with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "r") as f:
    onboarding_content = f.read()

old_onboarding_map = """    val leaguesByCountry = mapOf(
        "England" to listOf("Premier League", "Championship", "League One", "League Two"),
        "Italy" to listOf("Serie A", "Serie B"),
        "France" to listOf("Ligue 1", "Ligue 2"),
        "Germany" to listOf("Bundesliga", "Bundesliga 2", "3. Liga"),
        "Spain" to listOf("La Liga", "La Liga 2"),
        "Saudi" to listOf("Roshn Saudi League"),
        "America" to listOf("MLS"),
        "Portugal" to listOf("Liga Portugal"),
        "Netherlands" to listOf("Eredivisie")
    )"""

new_onboarding_map = """    val leaguesByCountry = mapOf(
        "England" to listOf("Premier League", "Championship", "League One", "League Two"),
        "Italy" to listOf("Serie A", "Serie B"),
        "France" to listOf("Ligue 1", "Ligue 2"),
        "Germany" to listOf("Bundesliga", "2. Bundesliga", "3. Liga"),
        "Spain" to listOf("La Liga", "Segunda División"),
        "Saudi" to listOf("Roshn Saudi League"),
        "America" to listOf("MLS", "USL Championship"),
        "USA" to listOf("MLS", "USL Championship"),
        "Brazil" to listOf("Brasileirão Série A", "Série B"),
        "Argentina" to listOf("Primera División"),
        "Portugal" to listOf("Liga Portugal"),
        "Netherlands" to listOf("Eredivisie")
    )"""
onboarding_content = onboarding_content.replace(old_onboarding_map, new_onboarding_map)

# Add USA, Brazil, Argentina to Onboarding countries
old_countries = """val countries = listOf("England", "Spain", "Italy", "Germany", "France", "Saudi", "America", "Portugal", "Netherlands", "Other")"""
new_countries = """val countries = listOf("England", "Spain", "Italy", "Germany", "France", "USA", "Brazil", "Argentina", "Saudi", "Portugal", "Netherlands", "Other")"""
onboarding_content = onboarding_content.replace(old_countries, new_countries)


with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "w") as f:
    f.write(onboarding_content)

