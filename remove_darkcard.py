with open('app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt', 'r') as f:
    text = f.read()

import re
text = re.sub(r'@Composable\nfun DarkCard\(modifier: Modifier = Modifier, content: @Composable ColumnScope\.\(\) -> Unit\) \{.*?\n\}\n', '', text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt', 'w') as f:
    f.write(text)

