import re

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    text = f.read()

# Replace the Box modifier in Dialog
text = text.replace('.fillMaxHeight(0.95f)\n                .clip(RoundedCornerShape(16.dp))', '.fillMaxHeight(0.95f)\n                .systemBarsPadding()\n                .clip(RoundedCornerShape(16.dp))')

# Also, since I already changed the bottom padding of the button to 48.dp, I should revert it to 16.dp or leave it.
# Let's revert it back to 16.dp so it looks balanced inside the box now that the box itself won't touch the nav bar.
text = text.replace('modifier = Modifier.fillMaxWidth().padding(start = 16.dp, end = 16.dp, top = 16.dp, bottom = 48.dp)', 'modifier = Modifier.fillMaxWidth().padding(16.dp)')

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write(text)
