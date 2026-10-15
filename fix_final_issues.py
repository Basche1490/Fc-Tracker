import re

# 1. Fix AssistantScreen.kt
with open("app/src/main/java/com/example/ui/screens/AssistantScreen.kt", "r") as f:
    ast_content = f.read()

ast_content = ast_content.replace(
    "val displayPlayers = viewingSeason?.players ?: displayPlayers",
    "val displayPlayers = viewingSeason?.players ?: state.players"
).replace(
    "val displayMatches = viewingSeason?.matches ?: displayMatches",
    "val displayMatches = viewingSeason?.matches ?: state.recentMatches"
).replace(
    "val displayTransfers = viewingSeason?.transfers ?: displayTransfers",
    "val displayTransfers = viewingSeason?.transfers ?: state.transfers"
).replace(
    "val displayYear = state.viewingSeasonYear ?: displayYear",
    "val displayYear = state.viewingSeasonYear ?: state.startYear"
)

with open("app/src/main/java/com/example/ui/screens/AssistantScreen.kt", "w") as f:
    f.write(ast_content)

# 2. Fix OnboardingScreen.kt
with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "r") as f:
    onb_content = f.read()

# We need to remove the duplicate `clubDomains`. There's one at the top (line 42) and one around line 238.
# Let's find the first `val clubDomains = mapOf(` and delete the entire block if there's a second one.
count_domains = onb_content.count("val clubDomains = mapOf(")
if count_domains > 1:
    # Delete the first one
    start = onb_content.find("val clubDomains = mapOf(")
    end = onb_content.find("val clubColors = mapOf(")
    if start != -1 and end != -1 and start < end:
        onb_content = onb_content[:start] + onb_content[end:]

with open("app/src/main/java/com/example/ui/screens/OnboardingScreen.kt", "w") as f:
    f.write(onb_content)

