import re

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "r") as f:
    content = f.read()

# Replace everything from val clubColors = mapOf( up to val countries =
start_idx = content.find("val clubColors = mapOf(")
end_idx = content.find("val countries = listOf(")

expanded = """val clubColors = mapOf(
        // ENGLAND
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
        "Leeds United" to ("#FFCD00" to "#1D428A"),
        "Leicester City" to ("#003090" to "#FDBE11"),
        "Southampton" to ("#D71920" to "#130C0E"),

        // SPAIN
        "Real Madrid" to ("#FFFFFF" to "#00529F"),
        "Barcelona" to ("#004D98" to "#A50044"),
        "Atletico Madrid" to ("#CB3524" to "#272E61"),
        "Sevilla" to ("#F43333" to "#FFFFFF"),
        "Real Sociedad" to ("#0067B1" to "#FFFFFF"),
        "Athletic Club" to ("#EE2523" to "#FFFFFF"),
        "Real Betis" to ("#0BB363" to "#FFFFFF"),
        "Valencia" to ("#FFFFFF" to "#000000"),
        "Villarreal" to ("#FCE216" to "#00508F"),
        "Girona" to ("#E63B2E" to "#FFFFFF"),

        // GERMANY
        "Bayern Munich" to ("#DC052D" to "#0066B2"),
        "Borussia Dortmund" to ("#FDE100" to "#000000"),
        "Bayer Leverkusen" to ("#E32221" to "#000000"),
        "RB Leipzig" to ("#DD013F" to "#002D54"),
        "Eintracht Frankfurt" to ("#E1000F" to "#000000"),
        "Stuttgart" to ("#E32221" to "#FFFFFF"),
        "Monchengladbach" to ("#000000" to "#FFFFFF"),
        "Wolfsburg" to ("#009F00" to "#FFFFFF"),

        // ITALY
        "Juventus" to ("#000000" to "#FFFFFF"),
        "AC Milan" to ("#FB090B" to "#000000"),
        "Inter Milan" to ("#010E80" to "#000000"),
        "Napoli" to ("#12A0D7" to "#FFFFFF"),
        "Roma" to ("#F0BC42" to "#8E1F2F"),
        "Lazio" to ("#87D8F7" to "#FFFFFF"),
        "Atalanta" to ("#19548E" to "#000000"),
        "Fiorentina" to ("#4A2583" to "#FFFFFF"),
        "Bologna" to ("#A32034" to "#1A2F4B"),

        // FRANCE
        "PSG" to ("#004170" to "#DA291C"),
        "Monaco" to ("#E32221" to "#FFFFFF"),
        "Marseille" to ("#2FAEE0" to "#FFFFFF"),
        "Lyon" to ("#DA0812" to "#003E7E"),
        "Lille" to ("#E01E13" to "#252B32"),
        "Lens" to ("#ED1C24" to "#FFD900"),
        "Nice" to ("#ED1C24" to "#000000"),
        "Rennes" to ("#ED1C24" to "#000000"),

        // SAUDI
        "Al Hilal" to ("#0055A5" to "#FFFFFF"),
        "Al Nassr" to ("#FFD700" to "#00205B"),
        "Al Ittihad" to ("#FCE300" to "#000000"),
        "Al Ahli" to ("#00A650" to "#FFFFFF"),
        "Al Ettifaq" to ("#006B3F" to "#E3001B"),

        // AMERICA
        "Inter Miami" to ("#F7B5CD" to "#000000"),
        "LA Galaxy" to ("#00245D" to "#FFD200"),
        "LAFC" to ("#000000" to "#C39E6D"),
        "Seattle Sounders" to ("#5D9732" to "#005587"),
        "Atlanta United" to ("#80000B" to "#221F1F"),
        "New York City FC" to ("#6CABDD" to "#00285E"),
        "Philadelphia Union" to ("#071B2C" to "#B18947"),
        
        // PORTUGAL
        "Benfica" to ("#ED1C24" to "#FFFFFF"),
        "Porto" to ("#00428C" to "#FFFFFF"),
        "Sporting CP" to ("#008057" to "#FFFFFF"),
        "Braga" to ("#E32221" to "#FFFFFF"),
        
        // NETHERLANDS
        "Ajax" to ("#D2122E" to "#FFFFFF"),
        "PSV" to ("#F11738" to "#FFFFFF"),
        "Feyenoord" to ("#EE2223" to "#000000"),
        "AZ Alkmaar" to ("#E32221" to "#FFFFFF")
    )

    val clubDomains = mapOf(
        // ENGLAND
        "Arsenal" to "arsenal.com",
        "Aston Villa" to "avfc.co.uk",
        "Bournemouth" to "afcb.co.uk",
        "Brentford" to "brentfordfc.com",
        "Brighton" to "brightonandhovealbion.com",
        "Burnley" to "burnleyfootballclub.com",
        "Chelsea" to "chelseafc.com",
        "Crystal Palace" to "cpfc.co.uk",
        "Everton" to "evertonfc.com",
        "Fulham" to "fulhamfc.com",
        "Liverpool" to "liverpoolfc.com",
        "Luton Town" to "lutontown.co.uk",
        "Manchester City" to "mancity.com",
        "Manchester United" to "manutd.com",
        "Newcastle United" to "nufc.co.uk",
        "Nottingham Forest" to "nottinghamforest.co.uk",
        "Sheffield United" to "sufc.co.uk",
        "Tottenham Hotspur" to "tottenhamhotspur.com",
        "West Ham" to "whufc.com",
        "Wolverhampton" to "wolves.co.uk",
        "Leeds United" to "leedsunited.com",
        "Leicester City" to "lcfc.com",
        "Southampton" to "southamptonfc.com",

        // SPAIN
        "Real Madrid" to "realmadrid.com",
        "Barcelona" to "fcbarcelona.com",
        "Atletico Madrid" to "atleticodemadrid.com",
        "Sevilla" to "sevillafc.es",
        "Real Sociedad" to "realsociedad.eus",
        "Athletic Club" to "athletic-club.eus",
        "Real Betis" to "realbetisbalompie.es",
        "Valencia" to "valenciacf.com",
        "Villarreal" to "villarrealcf.es",
        "Girona" to "gironafc.cat",

        // GERMANY
        "Bayern Munich" to "fcbayern.com",
        "Borussia Dortmund" to "bvb.de",
        "Bayer Leverkusen" to "bayer04.de",
        "RB Leipzig" to "rbleipzig.com",
        "Eintracht Frankfurt" to "eintracht.de",
        "Stuttgart" to "vfb.de",
        "Monchengladbach" to "borussia.de",
        "Wolfsburg" to "vfl-wolfsburg.de",

        // ITALY
        "Juventus" to "juventus.com",
        "AC Milan" to "acmilan.com",
        "Inter Milan" to "inter.it",
        "Napoli" to "sscnapoli.it",
        "Roma" to "asroma.com",
        "Lazio" to "sslazio.it",
        "Atalanta" to "atalanta.it",
        "Fiorentina" to "acffiorentina.com",
        "Bologna" to "bolognafc.it",

        // FRANCE
        "PSG" to "psg.fr",
        "Monaco" to "asmonaco.com",
        "Marseille" to "om.fr",
        "Lyon" to "ol.fr",
        "Lille" to "losc.fr",
        "Lens" to "rclens.fr",
        "Nice" to "ognice.com",
        "Rennes" to "staderennais.com",

        // SAUDI
        "Al Hilal" to "alhilal.com",
        "Al Nassr" to "alnassr.sa",
        "Al Ittihad" to "ittihadclub.sa",
        "Al Ahli" to "alahlifc.sa",
        "Al Ettifaq" to "ettifaq.com",

        // AMERICA
        "Inter Miami" to "intermiamicf.com",
        "LA Galaxy" to "lagalaxy.com",
        "LAFC" to "lafc.com",
        "Seattle Sounders" to "soundersfc.com",
        "Atlanta United" to "atlutd.com",
        "New York City FC" to "nycfc.com",
        "Philadelphia Union" to "philadelphiaunion.com",
        
        // PORTUGAL
        "Benfica" to "slbenfica.pt",
        "Porto" to "fcporto.pt",
        "Sporting CP" to "sporting.pt",
        "Braga" to "scbraga.pt",
        
        // NETHERLANDS
        "Ajax" to "ajax.nl",
        "PSV" to "psv.nl",
        "Feyenoord" to "feyenoord.nl",
        "AZ Alkmaar" to "az.nl"
    )

    """

new_content = content[:start_idx] + expanded + content[end_idx:]

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "w") as f:
    f.write(new_content)

