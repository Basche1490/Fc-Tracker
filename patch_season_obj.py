import re

with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "r") as f:
    content = f.read()

old_obj = """                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text(obj.category, fontSize = 10.sp, color = MaterialTheme.colorScheme.primary)
                                Text("Priority: ${obj.priority}", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                Text("Status: ${obj.status}", fontSize = 10.sp, color = when(obj.status) {
                                    "Completed" -> Color.Green
                                    "Failed" -> Color.Red
                                    else -> Color.Yellow
                                })
                            }"""

new_obj = """                            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text(obj.category, fontSize = 10.sp, color = MaterialTheme.colorScheme.primary)
                                Text("Priority: ${obj.priority}", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            Text("Status: ${obj.status}", fontSize = 10.sp, color = when(obj.status) {
                                "Completed" -> Color.Green
                                "Failed" -> Color.Red
                                else -> Color.Yellow
                            })"""

content = content.replace(old_obj, new_obj)

with open("app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt", "w") as f:
    f.write(content)

