import re

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "r") as f:
    content = f.read()

# Replace the clubDomains and selection logic with a more robust one.
new_selection = """                                        isExistingTeam = true
                                        val t = club.lowercase().replace(" ", "")
                                        val domain = when {
                                            clubDomains.containsKey(club) -> clubDomains[club]
                                            t.contains("arsenal") -> "arsenal.com"
                                            t.contains("astonvilla") -> "avfc.co.uk"
                                            t.contains("chelsea") -> "chelseafc.com"
                                            t.contains("everton") -> "evertonfc.com"
                                            t.contains("liverpool") -> "liverpoolfc.com"
                                            t.contains("mancity") || t.contains("manchestercity") -> "mancity.com"
                                            t.contains("manutd") || t.contains("manchesterunited") -> "manutd.com"
                                            t.contains("newcastle") -> "nufc.co.uk"
                                            t.contains("tottenham") || t.contains("spurs") -> "tottenhamhotspur.com"
                                            t.contains("realmadrid") -> "realmadrid.com"
                                            t.contains("barcelona") -> "fcbarcelona.com"
                                            t.contains("atletico") -> "en.atleticodemadrid.com"
                                            t.contains("bayern") -> "fcbayern.com"
                                            t.contains("dortmund") -> "bvb.de"
                                            t.contains("leverkusen") -> "bayer04.de"
                                            t.contains("juventus") -> "juventus.com"
                                            t.contains("milan") && !t.contains("inter") -> "acmilan.com"
                                            t.contains("inter") -> "inter.it"
                                            t.contains("napoli") -> "sscnapoli.it"
                                            t.contains("roma") -> "asroma.com"
                                            t.contains("psg") || t.contains("paris") -> "en.psg.fr"
                                            t.contains("marseille") -> "om.fr"
                                            t.contains("lyon") -> "ol.fr"
                                            t.contains("ajax") -> "english.ajax.nl"
                                            t.contains("psv") -> "psv.nl"
                                            t.contains("feyenoord") -> "feyenoord.com"
                                            t.contains("benfica") -> "slbenfica.pt"
                                            t.contains("porto") -> "fcporto.pt"
                                            t.contains("sporting") -> "sporting.pt"
                                            t.contains("alnassr") -> "alnassr.sa"
                                            t.contains("alhilal") -> "alhilal.com"
                                            t.contains("alittihad") -> "ittihadfc.com"
                                            t.contains("intermiami") -> "intermiamicf.com"
                                            t.contains("lagalaxy") -> "lagalaxy.com"
                                            t.contains("brighton") -> "brightonandhovealbion.com"
                                            t.contains("westham") -> "whufc.com"
                                            t.contains("crystalpalace") -> "cpfc.co.uk"
                                            t.contains("fulham") -> "fulhamfc.com"
                                            t.contains("brentford") -> "brentfordfc.com"
                                            t.contains("bournemouth") -> "afcb.co.uk"
                                            t.contains("wolverhampton") || t.contains("wolves") -> "wolves.co.uk"
                                            t.contains("nottingham") -> "nottinghamforest.co.uk"
                                            else -> t + ".com"
                                        }
                                        clubCrestUrl = "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://$domain&size=128"
                                        
                                        clubColors[club]?.let { colors ->
                                            primaryColor = colors.first
                                            secondaryColor = colors.second
                                        } ?: run {
                                            primaryColor = "#000000"
                                            secondaryColor = "#FFFFFF"
                                        }
                                        clubSearchExpanded = false"""

content = re.sub(r"isExistingTeam = true.*?clubSearchExpanded = false", new_selection, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "w") as f:
    f.write(content)

