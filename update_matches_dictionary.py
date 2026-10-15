import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

expanded_domains = """val clubDomains = mapOf(
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
    )"""

content = re.sub(r'val clubDomains = mapOf\([^\)]+\)', expanded_domains, content, count=1)

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

