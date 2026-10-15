with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()
    
# Find MatchResult data class and add motmName: String = ""
import re
new_match_result = r"val leaguePosition: Int = 1,\n    val motmName: String = \"\",\n    val playerPerformances:"
content = re.sub(r"val leaguePosition: Int = 1,\s*val playerPerformances:", new_match_result, content)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
