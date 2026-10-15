import re

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "r") as f:
    t_content = f.read()

# Replace transferDate init
target_date = "var transferDate by remember(logToEdit) { mutableStateOf(if (logToEdit?.date?.isNotEmpty() == true) logToEdit.date else java.text.SimpleDateFormat(\"yyyy-MM-dd\", java.util.Locale.getDefault()).apply { timeZone = java.util.TimeZone.getTimeZone(\"UTC\") }.format(java.util.Date())) }"
replacement_date = """var transferDate by remember(logToEdit) { 
        mutableStateOf(
            if (logToEdit?.date?.isNotEmpty() == true) logToEdit.date 
            else {
                val cal = java.util.Calendar.getInstance(java.util.TimeZone.getTimeZone("UTC"))
                cal.set(java.util.Calendar.YEAR, state.startYear)
                val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).apply { timeZone = java.util.TimeZone.getTimeZone("UTC") }
                sdf.format(cal.time)
            }
        ) 
    }"""
t_content = t_content.replace(target_date, replacement_date)

# Replace datePickerState to use transferDate as initial
target_dp = "val datePickerState = rememberDatePickerState()"
replacement_dp = """val initialMillis = remember(transferDate) {
                                try {
                                    val sdf = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.getDefault()).apply { timeZone = java.util.TimeZone.getTimeZone("UTC") }
                                    sdf.parse(transferDate)?.time
                                } catch (e: Exception) { null }
                            }
                            val datePickerState = rememberDatePickerState(initialSelectedDateMillis = initialMillis, initialDisplayedMonthMillis = initialMillis)"""
t_content = t_content.replace(target_dp, replacement_dp)

with open("app/src/main/java/com/example/ui/screens/TransfersScreen.kt", "w") as f:
    f.write(t_content)


with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    s_content = f.read()

target_squad = """            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "${player.displayName}",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onBackground
                )
                Text(
                    text = "${player.primaryPosition} • Age ${player.age}",
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "€${player.valueM}M • €${player.wageK}K/wk",
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Bold
                )
                val tags = mutableListOf<String>()
                if (player.isLoanedOut) tags.add("Out on Loan")
                if (player.isLoanedIn) tags.add("Loaned In")
                if (player.isRegen) tags.add("Regen")
                if (player.isPromoted) tags.add("Promoted")
                if (player.isAcademy) tags.add("Academy")
                if (player.isInjured) tags.add("Injured")
                if (tags.isNotEmpty()) {
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.padding(top = 4.dp)) {
                        tags.forEach { tag ->
                            val bgColor = if (tag == "Injured") Color.Red.copy(alpha=0.7f) else MaterialTheme.colorScheme.secondary.copy(alpha = 0.7f)
                            Text(tag, fontSize = 8.sp, color = Color.White, modifier = Modifier.background(bgColor, RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp))
                        }
                    }
                }
            }"""

replacement_squad = """            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = "${player.displayName}",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onBackground
                    )
                    val tags = mutableListOf<String>()
                    if (player.isLoanedOut) tags.add("Out on Loan")
                    if (player.isLoanedIn) tags.add("Loaned In")
                    if (player.isRegen) tags.add("Regen")
                    if (player.isPromoted) tags.add("Promoted")
                    if (player.isAcademy) tags.add("Academy")
                    if (player.isInjured) tags.add("Injured")
                    if (tags.isNotEmpty()) {
                        Spacer(modifier = Modifier.width(8.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                            tags.forEach { tag ->
                                val bgColor = if (tag == "Injured") Color.Red.copy(alpha=0.7f) else MaterialTheme.colorScheme.secondary.copy(alpha = 0.7f)
                                Text(tag, fontSize = 8.sp, color = Color.White, modifier = Modifier.background(bgColor, RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp))
                            }
                        }
                    }
                }
                Text(
                    text = "${player.primaryPosition} • Age ${player.age}",
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "€${player.valueM}M • €${player.wageK}K/wk",
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Bold
                )
            }"""

s_content = s_content.replace(target_squad, replacement_squad)

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(s_content)

print("Done")

