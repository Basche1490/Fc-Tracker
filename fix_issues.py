import os
import re

# 1. Fix images (replace icon.horse with gstatic)
def replace_images(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    content = content.replace("https://icon.horse/icon/$domain", "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://$domain&size=256")
    content = content.replace("https://icon.horse/icon/${exactMatch.value}", "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${exactMatch.value}&size=256")
    content = content.replace("https://icon.horse/icon/${domain}", "https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${domain}&size=256")
    with open(file_path, "w") as f:
        f.write(content)

for root, dirs, files in os.walk("app/src/main/java/com/example/ui/screens"):
    for file in files:
        if file.endswith(".kt"):
            replace_images(os.path.join(root, file))

# 2. Fix MatchesScreen currentMonthCal
with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
"""    var currentMonthCal by remember { 
        mutableStateOf(
            if (displayMatches.isNotEmpty()) {
                val latest = displayMatches.first().matchDate
                try {
                    val d = df.parse(latest)
                    Calendar.getInstance().apply { time = d; set(Calendar.DAY_OF_MONTH, 1) }
                } catch(e: Exception) {
                    startCal.clone() as Calendar
                }
            } else {
                startCal.clone() as Calendar
            }
        ) 
    }""",
"""    var currentMonthCal by remember(displayMatches.size) { 
        mutableStateOf(
            if (displayMatches.isNotEmpty()) {
                val latest = displayMatches.first().matchDate
                try {
                    val d = df.parse(latest)
                    if (d != null) {
                        Calendar.getInstance(TimeZone.getTimeZone("UTC")).apply { time = d; set(Calendar.DAY_OF_MONTH, 1) }
                    } else {
                        startCal.clone() as Calendar
                    }
                } catch(e: Exception) {
                    startCal.clone() as Calendar
                }
            } else {
                startCal.clone() as Calendar
            }
        ) 
    }""")

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(content)

print("Finished fixing images and MatchesScreen")
