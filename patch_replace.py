import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# 1. Update MatchResultCard Competition Logo
old_comp = r"""coil\.compose\.AsyncImage\(\s*model = "https://ui-avatars\.com/api/\?name=\$\{match\.competition\.replace\(" ", "\+"\)\}&background=random&color=fff&size=128",\s*contentDescription = "Competition Logo",\s*modifier = Modifier\.size\(32\.dp\)\.clip\(CircleShape\)\s*\)"""
new_comp = """CompetitionLogoImage(competition = match.competition, modifier = Modifier.size(32.dp).clip(CircleShape))"""
content = re.sub(old_comp, new_comp, content)

# 2. Update MatchFormModal Opponent Logo
old_opp_logo = r"""                                if \(opponentCrestUrl\.isNotBlank\(\)\) \{.*?Text\(if \(opponent\.isBlank\(\)\) "Select Opponent" else opponent, fontSize = 14\.sp, fontWeight = FontWeight\.Bold, color = Color\.White, textAlign = TextAlign\.Center\)"""
new_opp_logo = """                                TeamCrestImage(teamName = opponent, modifier = Modifier.size(64.dp).clip(CircleShape))
                                Spacer(Modifier.height(8.dp))
                                Text(if (opponent.isBlank()) "Select Opponent" else opponent, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White, textAlign = TextAlign.Center)"""
content = re.sub(old_opp_logo, new_opp_logo, content, flags=re.DOTALL)

# 3. Update Suggestions List in Opponent Dialog
old_suggs = r"""val suggestions = listOf\("Arsenal".*?"Paris Saint-Germain"\)"""
new_suggs = """val suggestions = listOf(
                                            "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Burnley", "Chelsea", "Crystal Palace", "Everton", "Fulham", "Liverpool", "Luton Town", "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest", "Sheffield United", "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers",
                                            "Real Madrid", "Barcelona", "Atletico Madrid", "Girona", "Real Sociedad", "Athletic Bilbao", "Real Betis", "Valencia", "Villarreal", "Sevilla",
                                            "Inter Milan", "AC Milan", "Juventus", "AS Roma", "Napoli", "Lazio", "Atalanta", "Fiorentina", "Bologna", "Torino",
                                            "Bayern Munich", "Borussia Dortmund", "Bayer Leverkusen", "RB Leipzig", "VfB Stuttgart", "Eintracht Frankfurt", "Borussia Monchengladbach", "Wolfsburg",
                                            "Paris Saint-Germain", "Monaco", "Marseille", "Lille", "Lyon", "Lens", "Nice", "Rennes",
                                            "Ajax", "PSV Eindhoven", "Feyenoord", "Sporting CP", "Benfica", "Porto", "Galatasaray", "Fenerbahce", "Besiktas", "Celtic", "Rangers"
                                        ).sorted()"""
content = re.sub(old_suggs, new_suggs, content)

# 4. Update MOTM Suggestions List
old_motm = r"""val allOptions = state\.players\.map \{ it\.displayName \} \+ listOf\("Opponent Player"\)"""
new_motm = """val topRealPlayers = listOf(
                                    "Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappé", "Erling Haaland", "Kevin De Bruyne", "Mohamed Salah", "Harry Kane", "Jude Bellingham", "Vinícius Júnior", "Rodri", "Bernardo Silva", "Virgil van Dijk", "Alisson", "Thibaut Courtois", "Luka Modric", "Toni Kroos", "Robert Lewandowski", "Antoine Griezmann", "Bukayo Saka", "Phil Foden", "Declan Rice", "Martin Ødegaard", "Son Heung-min", "Victor Osimhen", "Rafael Leão", "Khvicha Kvaratskhelia", "Lautaro Martínez", "Marcus Rashford", "Bruno Fernandes", "Jamal Musiala", "Florian Wirtz", "Xavi Simons"
                                )
                                val allOptions = state.players.map { it.displayName } + topRealPlayers + listOf("Opponent Player")"""
content = re.sub(old_motm, new_motm, content)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
