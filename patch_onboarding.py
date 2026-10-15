import re

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "r") as f:
    content = f.read()

# Update club colors map
old_colors = """    val clubColors = mapOf(
        "Arsenal" to ("#EF0107" to "#063672"),
        "Aston Villa" to ("#670E36" to "#95BFE5"),
        "Chelsea" to ("#034694" to "#EE242C"),
        "Everton" to ("#003399" to "#FFFFFF"),
        "Liverpool" to ("#C8102E" to "#F6EB61"),
        "Manchester City" to ("#6CABDD" to "#1C2C5B"),
        "Manchester United" to ("#DA291C" to "#FBE122"),
        "Newcastle United" to ("#241F20" to "#F1F1F1"),
        "Tottenham Hotspur" to ("#132257" to "#FFFFFF"),
        "Real Madrid" to ("#FFFFFF" to "#00529F"),
        "Barcelona" to ("#004D98" to "#A50044"),
        "Atletico Madrid" to ("#CB3524" to "#272E61"),
        "Bayern Munich" to ("#DC052D" to "#0066B2"),
        "Borussia Dortmund" to ("#FDE100" to "#000000"),
        "Bayer Leverkusen" to ("#E32221" to "#000000"),
        "Juventus" to ("#000000" to "#FFFFFF"),
        "AC Milan" to ("#FB090B" to "#000000"),
        "Inter Milan" to ("#010E80" to "#000000"),
        "Napoli" to ("#12A0D7" to "#FFFFFF"),
        "Roma" to ("#F0BC42" to "#8E1F2F"),
        "PSG" to ("#004170" to "#DA291C")
    )"""

new_colors = """    val clubColors = mapOf(
        "Arsenal" to ("#EF0107" to "#063672"),
        "Aston Villa" to ("#670E36" to "#95BFE5"),
        "Bournemouth" to ("#B50E12" to "#000000"),
        "Brentford" to ("#E30613" to "#000000"),
        "Brighton" to ("#0057B8" to "#FFFFFF"),
        "Burnley" to ("#6C1D45" to "#99D6EA"),
        "Chelsea" to ("#034694" to "#EE242C"),
        "Crystal Palace" to ("#1B458F" to "#A7A5A6"),
        "Everton" to ("#003399" to "#FFFFFF"),
        "Fulham" to ("#FFFFFF" to "#000000"),
        "Liverpool" to ("#C8102E" to "#00B2A9"),
        "Luton Town" to ("#F78F1E" to "#000099"),
        "Manchester City" to ("#6CABDD" to "#1C2C5B"),
        "Manchester United" to ("#DA291C" to "#FBE122"),
        "Newcastle United" to ("#241F20" to "#F1F1F1"),
        "Nottingham Forest" to ("#E53233" to "#FFFFFF"),
        "Sheffield United" to ("#EE2737" to "#000000"),
        "Tottenham Hotspur" to ("#132257" to "#FFFFFF"),
        "West Ham" to ("#7A263A" to "#1BB1E7"),
        "Wolverhampton" to ("#FDB913" to "#231F20"),
        "Real Madrid" to ("#FFFFFF" to "#00529F"),
        "Barcelona" to ("#004D98" to "#A50044"),
        "Atletico Madrid" to ("#CB3524" to "#272E61"),
        "Bayern Munich" to ("#DC052D" to "#0066B2"),
        "Borussia Dortmund" to ("#FDE100" to "#000000"),
        "Bayer Leverkusen" to ("#E32221" to "#000000"),
        "Juventus" to ("#000000" to "#FFFFFF"),
        "AC Milan" to ("#FB090B" to "#000000"),
        "Inter Milan" to ("#010E80" to "#000000"),
        "Napoli" to ("#12A0D7" to "#FFFFFF"),
        "Roma" to ("#F0BC42" to "#8E1F2F"),
        "PSG" to ("#004170" to "#DA291C"),
        "Monaco" to ("#E32221" to "#FFFFFF")
    )"""
content = content.replace(old_colors, new_colors)

# Update fallback colors
old_fallback = """                                        } ?: run {
                                            primaryColor = "#000000"
                                            secondaryColor = "#FFFFFF"
                                        }"""
new_fallback = """                                        } ?: run {
                                            primaryColor = "#546E7A"
                                            secondaryColor = "#FFC107"
                                        }"""
content = content.replace(old_fallback, new_fallback)

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "w") as f:
    f.write(content)

