import re

def rewrite():
    # Fix FormationTab.kt
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
        content = f.read()
    content = content.replace("val positions = listOfNotNull(player.primaryPosition, player.secondaryPosition).joinToString(\",\")", 
                              "val positions = listOfNotNull(player.primaryPosition, player.secondaryPosition).filter { it.isNotBlank() }.joinToString(\",\")")
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
        f.write(content)

    # Fix MatchesScreen.kt
    with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
        content = f.read()
    content = content.replace("val positions = listOfNotNull(player?.primaryPosition, player?.secondaryPosition, player?.tertiaryPosition).map { it.uppercase() }",
                              "val positions = listOfNotNull(player?.primaryPosition, player?.secondaryPosition, player?.tertiaryPosition).filter { it.isNotBlank() }.map { it.uppercase() }")
    with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
        f.write(content)

rewrite()
