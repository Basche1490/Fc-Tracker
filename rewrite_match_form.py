import re

with open('app/src/main/java/com/example/ui/screens/MatchesScreen.kt', 'r') as f:
    text = f.read()

text = text.replace('"Champions League", "Europa League"', '"Champions League", "Europa League", "Conference League"')

# Find the Away Name and Crest box
away_box = """                        Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.weight(1f)) {
                            val awayCrest = if (!isHome) state.clubCrestUrl else opponentCrestUrl
                            val awayName = if (!isHome) state.clubName else opponentName
                            if (awayCrest.isNotEmpty()) {
                                coil.compose.AsyncImage(model = awayCrest, contentDescription = null, modifier = Modifier.size(48.dp).clip(CircleShape))
                            } else {
                                Box(modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) { Text(awayName.take(2), color = Color.White) }
                            }
                            Text(awayName, fontSize = 12.sp, color = Color.White, maxLines = 1, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                        }"""

new_away_box = """                        var showTeamSearch by remember { mutableStateOf(false) }
                        Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.weight(1f).clickable { showTeamSearch = true }) {
                            val awayCrest = if (!isHome) state.clubCrestUrl else opponentCrestUrl
                            val awayName = if (!isHome) state.clubName else if (opponentName.isEmpty()) "Select Opponent" else opponentName
                            if (awayCrest.isNotEmpty()) {
                                coil.compose.AsyncImage(model = awayCrest, contentDescription = null, modifier = Modifier.size(48.dp).clip(CircleShape))
                            } else {
                                Box(modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) { Text(awayName.take(2), color = Color.White) }
                            }
                            Text(awayName, fontSize = 12.sp, color = Color.White, maxLines = 1, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                        }
                        
                        if (showTeamSearch) {
                            Dialog(onDismissRequest = { showTeamSearch = false }) {
                                Box(modifier = Modifier.fillMaxWidth().heightIn(max=400.dp).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surface).padding(16.dp)) {
                                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Text("Search Opponent Team", color = Color.White, fontWeight = FontWeight.Bold)
                                        var teamQuery by remember { mutableStateOf("") }
                                        OutlinedTextField(value = teamQuery, onValueChange = { teamQuery = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Search") })
                                        val results = viewModel.searchPlayersAndTeams(teamQuery).map { it.team }.distinct().take(10)
                                        LazyColumn {
                                            items(results) { t ->
                                                Text(t, color = Color.White, modifier = Modifier.fillMaxWidth().clickable {
                                                    opponentName = t
                                                    opponentCrestUrl = "https://logo.clearbit.com/${t.replace(" ", "").lowercase()}.com"
                                                    showTeamSearch = false
                                                }.padding(12.dp))
                                            }
                                        }
                                    }
                                }
                            }
                        }"""

text = text.replace(away_box, new_away_box)

# We also need to do it for Home Team, since Home could be the opponent
home_box = """                        Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.weight(1f)) {
                            val homeCrest = if (isHome) state.clubCrestUrl else opponentCrestUrl
                            val homeName = if (isHome) state.clubName else opponentName
                            if (homeCrest.isNotEmpty()) {
                                coil.compose.AsyncImage(model = homeCrest, contentDescription = null, modifier = Modifier.size(48.dp).clip(CircleShape))
                            } else {
                                Box(modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) { Text(homeName.take(2), color = Color.White) }
                            }
                            Text(homeName, fontSize = 12.sp, color = Color.White, maxLines = 1, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                        }"""

new_home_box = """                        var showHomeTeamSearch by remember { mutableStateOf(false) }
                        Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.weight(1f).clickable { showHomeTeamSearch = true }) {
                            val homeCrest = if (isHome) state.clubCrestUrl else opponentCrestUrl
                            val homeName = if (isHome) state.clubName else if (opponentName.isEmpty()) "Select Opponent" else opponentName
                            if (homeCrest.isNotEmpty()) {
                                coil.compose.AsyncImage(model = homeCrest, contentDescription = null, modifier = Modifier.size(48.dp).clip(CircleShape))
                            } else {
                                Box(modifier = Modifier.size(48.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) { Text(homeName.take(2), color = Color.White) }
                            }
                            Text(homeName, fontSize = 12.sp, color = Color.White, maxLines = 1, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                        }
                        
                        if (showHomeTeamSearch) {
                            Dialog(onDismissRequest = { showHomeTeamSearch = false }) {
                                Box(modifier = Modifier.fillMaxWidth().heightIn(max=400.dp).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surface).padding(16.dp)) {
                                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Text("Search Opponent Team", color = Color.White, fontWeight = FontWeight.Bold)
                                        var teamQuery by remember { mutableStateOf("") }
                                        OutlinedTextField(value = teamQuery, onValueChange = { teamQuery = it }, modifier = Modifier.fillMaxWidth(), label = { Text("Search") })
                                        val results = viewModel.searchPlayersAndTeams(teamQuery).map { it.team }.distinct().take(10)
                                        LazyColumn {
                                            items(results) { t ->
                                                Text(t, color = Color.White, modifier = Modifier.fillMaxWidth().clickable {
                                                    opponentName = t
                                                    opponentCrestUrl = "https://logo.clearbit.com/${t.replace(" ", "").lowercase()}.com"
                                                    showHomeTeamSearch = false
                                                }.padding(12.dp))
                                            }
                                        }
                                    }
                                }
                            }
                        }"""

text = text.replace(home_box, new_home_box)

# Now remove the old Opponent club name and crest URL fields.
# We will use regex to remove them because they are complex ExposedDropdownMenuBox.

remove_regex = r'item \{\s*var teamQuery by remember \{ mutableStateOf\(opponentName\) \}.*?\}\s*\}\s*item \{ OutlinedTextField\(value = opponentCrestUrl, onValueChange = \{ opponentCrestUrl = it \}, label = \{ Text\("Opponent Crest URL \(Optional\)"\) \}, modifier = Modifier\.fillMaxWidth\(\)\) \}'
text = re.sub(remove_regex, '', text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/MatchesScreen.kt', 'w') as f:
    f.write(text)
