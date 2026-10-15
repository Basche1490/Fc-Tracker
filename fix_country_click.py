with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

old_click = """                                        onClick = {
                                            country = selectionOption
                                            countryExpanded = false
                                        }"""

new_click = """                                        onClick = {
                                            country = selectionOption
                                            val newLeagues = leaguesByCountry[selectionOption]
                                            if (newLeagues != null && !newLeagues.contains(leagueName)) {
                                                leagueName = newLeagues[0]
                                            }
                                            countryExpanded = false
                                        }"""

content = content.replace(old_click, new_click)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
