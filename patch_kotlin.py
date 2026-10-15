import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    code = f.read()

# Update GoalDetail data class
code = re.sub(
    r'data class GoalDetail\(\s+val minute: Int = 0,',
    r'data class GoalDetail(\n    val minute: Int? = null,',
    code
)

# Update parseMatchPerformances
code = re.sub(
    r'rating = p\.optDouble\("rating", 7\.0\),\s+subInMinute = if \(p\.optBoolean\("isSub"\)\) 45 else null',
    r'rating = 0.0',
    code
)

# Update parseGoalDetails
code = re.sub(
    r'minute = p\.optInt\("minute"\)',
    r'minute = if (p.has("minute")) p.optInt("minute") else null',
    code
)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(code)

print("Patched MainViewModel!")
