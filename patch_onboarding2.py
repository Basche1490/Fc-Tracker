import re

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "r") as f:
    content = f.read()

content = content.replace("fun OnboardingScreen(", "fun OnboardingScreen(viewModel: com.example.MainViewModel, ")

old_clubs = """    val realClubs = listOf("Arsenal", "Aston Villa", "Chelsea", "Everton", "Liverpool", "Manchester City", "Manchester United", "Newcastle United", "Tottenham Hotspur", "Real Madrid", "Barcelona", "Atletico Madrid", "Bayern Munich", "Borussia Dortmund", "Bayer Leverkusen", "Juventus", "AC Milan", "Inter Milan", "Napoli", "Roma", "Paris Saint-Germain", "Marseille", "Lyon", "Ajax", "PSV", "Feyenoord", "Benfica", "Porto", "Sporting CP", "Al Nassr", "Al Hilal", "Al Ittihad", "Inter Miami", "LA Galaxy")"""

new_clubs = """    var realClubs by remember { mutableStateOf(emptyList<String>()) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.Dispatchers.IO.invoke {
            val clubs = viewModel.getUniqueClubs()
            realClubs = clubs
        }
    }"""

content = content.replace(old_clubs, new_clubs)

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "w") as f:
    f.write(content)

