import sys
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

# Fix newline split
content = content.replace('val lines = response.split("\n")', 'val lines = response.lines()')

# Fix isActive
content = content.replace('kotlinx.coroutines.isActive', 'kotlinx.coroutines.isActive')
content = "import kotlinx.coroutines.isActive\n" + content

# Fix resultBadge
content = content.replace('resultBadge = dataObj.optString("resultBadge"),', '')

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
