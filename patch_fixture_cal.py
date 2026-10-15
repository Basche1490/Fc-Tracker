import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

# Fix FixtureCalendar definition if not fixed
if "onDateClick: (MatchResult) -> Unit" not in content:
    content = content.replace(
        "matches: List<MatchResult>\n) {", 
        "matches: List<MatchResult>,\n    onDateClick: (MatchResult) -> Unit\n) {"
    )
    content = content.replace(
        "matches: List<MatchResult>) {", 
        "matches: List<MatchResult>,\n    onDateClick: (MatchResult) -> Unit\n) {"
    )

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)
