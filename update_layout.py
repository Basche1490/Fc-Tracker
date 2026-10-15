import re

with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
    content = f.read()

# Update the bench Card modifier
old_bench_card = "Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {"
new_bench_card = "Card(modifier = Modifier.fillMaxWidth().heightIn(max = 220.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {"
content = content.replace(old_bench_card, new_bench_card)

# Update the bench Column to be scrollable
old_bench_column = "Column(verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp)) {"
new_bench_column = "Column(verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp).verticalScroll(rememberScrollState())) {"
content = content.replace(old_bench_column, new_bench_column)

# Make sure we import verticalScroll and rememberScrollState
if "import androidx.compose.foundation.verticalScroll" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.verticalScroll\nimport androidx.compose.foundation.rememberScrollState")

with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
    f.write(content)

