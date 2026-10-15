with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

old_currency = """                        OutlinedTextField(value = currencySymbol, onValueChange = { currencySymbol = it }, label = { Text("Currency") }, modifier = Modifier.weight(1f), singleLine = true)"""

new_currency = """                        var currencyExpanded by remember { mutableStateOf(false) }
                        val currencies = listOf("€ - EUR", "£ - GBP", "$ - USD")
                        ExposedDropdownMenuBox(
                            expanded = currencyExpanded,
                            onExpandedChange = { currencyExpanded = !currencyExpanded },
                            modifier = Modifier.weight(1f)
                        ) {
                            OutlinedTextField(
                                value = currencySymbol,
                                onValueChange = {},
                                readOnly = true,
                                label = { Text("Currency") },
                                modifier = Modifier.fillMaxWidth().menuAnchor(),
                                singleLine = true,
                                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = currencyExpanded) },
                                colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors()
                            )
                            ExposedDropdownMenu(
                                expanded = currencyExpanded,
                                onDismissRequest = { currencyExpanded = false }
                            ) {
                                currencies.forEach { selectionOption ->
                                    DropdownMenuItem(
                                        text = { Text(selectionOption) },
                                        onClick = {
                                            currencySymbol = selectionOption
                                            currencyExpanded = false
                                        }
                                    )
                                }
                            }
                        }"""

content = content.replace(old_currency, new_currency)

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
    f.write(content)
