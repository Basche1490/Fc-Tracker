import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    content = f.read()

target = """                                val clubDomains = mapOf(
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
        "Feyenoord" to "feyenoord.com",
        "Benfica" to "slbenfica.pt",
        "Porto" to "fcporto.pt",
        "Sporting CP" to "sporting.pt",
        "Al Nassr" to "alnassr.sa",
        "Al Hilal" to "alhilal.com",
        "Al Ittihad" to "ittihadclub.sa",
        "Inter Miami" to "intermiamicf.com",
        "LA Galaxy" to "lagalaxy.com"
    )
                            val cleanClubName = log.fromToClub.replace(" ", "").lowercase()
                            val domain = clubDomains[log.fromToClub] ?: "${cleanClubName}.com"
                            val crestUrl = "https://icon.horse/icon/$domain"
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant),
                                contentAlignment = Alignment.Center
                            ) {
                                coil.compose.SubcomposeAsyncImage(
                                    model = crestUrl,
                                    contentDescription = "Club Crest",
                                    modifier = Modifier.fillMaxSize(),
                                    contentScale = androidx.compose.ui.layout.ContentScale.Fit,
                                    error = {
                                        Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxSize()) {
                                            Text(log.fromToClub.split(" ").mapNotNull { it.firstOrNull() }.joinToString("").take(2).uppercase(), color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                        }
                                    }
                                )
                            }"""

replacement = """                            val playerObj = state.players.find { it.name == log.playerName || it.displayName == log.playerName }
                            val headshotUrl = playerObj?.headshotUrl?.takeIf { it.isNotBlank() } ?: "https://ui-avatars.com/api/?name=${log.playerName.replace(" ", "+")}&background=random&color=fff&size=256"
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .clip(androidx.compose.foundation.shape.CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant),
                                contentAlignment = Alignment.Center
                            ) {
                                coil.compose.SubcomposeAsyncImage(
                                    model = headshotUrl,
                                    contentDescription = "Player Headshot",
                                    modifier = Modifier.fillMaxSize(),
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    error = {
                                        Box(contentAlignment = Alignment.Center, modifier = Modifier.fillMaxSize()) {
                                            Text(log.playerName.take(1).uppercase(), color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                        }
                                    }
                                )
                            }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
        f.write(content)
    print("Replaced crest with player image")
else:
    print("Could not find crest block")

