with open('app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt', 'r') as f:
    text = f.read()

text = text.replace('Text("Trust Level: ${if (percentage > 0.6) \\"High\\" else \\"Low\\"}", color = MaterialTheme.colorScheme.onSurfaceVariant)', 'Text(if (percentage > 0.6f) "Trust Level: High" else "Trust Level: Low", color = MaterialTheme.colorScheme.onSurfaceVariant)')
text = text.replace('Text("Trust Level: ${if (percentage > 0.6) \\"High\\" else \\"Low\\"}"', 'Text(if (percentage > 0.6f) "Trust Level: High" else "Trust Level: Low"')

# In Kotlin, we can't do this inside string interpolation if we escaped quotes incorrectly
import re
text = re.sub(r'Text\("Trust Level: \$\{if \(percentage > 0\.6\) \\"High\\" else \\"Low\\"\}"', r'Text(if (percentage > 0.6f) "Trust Level: High" else "Trust Level: Low"', text)
text = re.sub(r'Text\("Trust Level: \$\{if \(percentage > 0\.6\) "High" else "Low"\}"', r'Text(if (percentage > 0.6f) "Trust Level: High" else "Trust Level: Low"', text)

if 'fun DarkCard' not in text:
    text += "\n@Composable\nfun DarkCard(modifier: Modifier = Modifier, content: @Composable ColumnScope.() -> Unit) {\n    Box(\n        modifier = modifier.clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surface).border(1.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(16.dp)).padding(16.dp)\n    ) {\n        Column(content = content)\n    }\n}\n"

with open('app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt', 'w') as f:
    f.write(text)
