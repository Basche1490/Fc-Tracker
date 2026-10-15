with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

# Fix the duplicate annotations and placement
bad_str = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
    val leaguesByCountry"""

good_str = """    val leaguesByCountry"""

content = content.replace(bad_str, good_str)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
