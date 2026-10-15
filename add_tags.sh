sed -i '/text = "€${player.valueM}M • €${player.wageK}K\/wk",/!b;n;n;n;a \
                val tags = mutableListOf<String>()\
                if (player.isLoanedOut) tags.add("Out on Loan")\
                if (player.isLoanedIn) tags.add("Loaned In")\
                if (player.isRegen) tags.add("Regen")\
                if (player.isAcademy) tags.add("Academy")\
                if (player.isInjured) tags.add("Injured")\
                if (tags.isNotEmpty()) {\
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.padding(top = 4.dp)) {\
                        tags.forEach { tag ->\
                            val bgColor = if (tag == "Injured") Color.Red.copy(alpha=0.7f) else MaterialTheme.colorScheme.secondary.copy(alpha = 0.7f)\
                            Text(tag, fontSize = 8.sp, color = Color.White, modifier = Modifier.background(bgColor, RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp))\
                        }\
                    }\
                }' app/src/main/java/com/example/ui/screens/SquadScreen.kt
