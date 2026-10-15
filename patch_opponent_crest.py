import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# Fix the opponent dialog overriding the URL
old_dialog = r"""                                                Row\(modifier = Modifier\.fillMaxWidth\(\)\.clickable \{ 
                                                    opponent = team
                                                    opponentCrestUrl = "https://ui-avatars\.com/api/\?name=\$\{team\.replace\(" ", "\+"\)\}&background=random&color=fff&size=256"
                                                    showOpponentDialog = false 
                                                \}\.padding\(vertical = 8\.dp\)\) \{
                                                    Text\(team, color = Color\.White\)
                                                \}"""

new_dialog = """                                                Row(modifier = Modifier.fillMaxWidth().clickable { 
                                                    opponent = team
                                                    opponentCrestUrl = getTeamCrestUrl(team)
                                                    showOpponentDialog = false 
                                                }.padding(vertical = 8.dp)) {
                                                    Text(team, color = Color.White)
                                                }"""

content = re.sub(old_dialog, new_dialog, content)

old_custom_button = r"""                                                Button\(onClick = \{ 
                                            opponentCrestUrl = "https://ui-avatars\.com/api/\?name=\$\{opponent\.replace\(" ", "\+"\)\}&background=random&color=fff&size=256"
                                            showOpponentDialog = false 
                                        \}, modifier = Modifier\.fillMaxWidth\(\)\) \{
                                            Text\("Set Custom Team"\)
                                        \}"""

new_custom_button = """                                                Button(onClick = { 
                                            opponentCrestUrl = getTeamCrestUrl(opponent)
                                            showOpponentDialog = false 
                                        }, modifier = Modifier.fillMaxWidth()) {
                                            Text("Set Custom Team")
                                        }"""

content = re.sub(old_custom_button, new_custom_button, content)

# Add the crest to MatchResultCard
old_card_header = r"""                    CompetitionLogoImage\(competition = match\.competition, modifier = Modifier\.size\(32\.dp\)\.clip\(CircleShape\)\)
                    Spacer\(Modifier\.width\(8\.dp\)\)
                    Box\("""

new_card_header = """                    CompetitionLogoImage(competition = match.competition, modifier = Modifier.size(32.dp).clip(CircleShape))
                    Spacer(Modifier.width(8.dp))
                    TeamCrestImage(teamName = match.opponentName, modifier = Modifier.size(32.dp).clip(CircleShape))
                    Spacer(Modifier.width(8.dp))
                    Box("""

content = re.sub(old_card_header, new_card_header, content)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
