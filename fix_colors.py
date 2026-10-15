import re

with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "r") as f:
    content = f.read()

color_pickers_old = """
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = primaryColorHex, 
                            onValueChange = { primaryColorHex = it }, 
                            label = { Text("Primary Color") }, 
                            modifier = Modifier.weight(1f), 
                            singleLine = true,
                            trailingIcon = {
                                IconButton(onClick = { showPrimaryColorPicker = true }) {
                                    Icon(Icons.Default.Edit, contentDescription = "Pick Color")
                                }
                            }
                        )
                        OutlinedTextField(
                            value = secondaryColorHex, 
                            onValueChange = { secondaryColorHex = it }, 
                            label = { Text("Secondary Color") }, 
                            modifier = Modifier.weight(1f), 
                            singleLine = true,
                            trailingIcon = {
                                IconButton(onClick = { showSecondaryColorPicker = true }) {
                                    Icon(Icons.Default.Edit, contentDescription = "Pick Color")
                                }
                            }
                        )
                    }
                    
                    if (showPrimaryColorPicker) {
                        Dialog(onDismissRequest = { showPrimaryColorPicker = false }) {
                            DarkCard(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Text("Select Primary Color", color = Color.White, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(16.dp))
                                Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
                                    ColorWheel(modifier = Modifier.fillMaxSize()) { color ->
                                        primaryColorHex = color.toHexCode()
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Button(onClick = { showPrimaryColorPicker = false }, modifier = Modifier.fillMaxWidth()) {
                                    Text("Done")
                                }
                            }
                        }
                    }
                    if (showSecondaryColorPicker) {
                        Dialog(onDismissRequest = { showSecondaryColorPicker = false }) {
                            DarkCard(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Text("Select Secondary Color", color = Color.White, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(16.dp))
                                Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
                                    ColorWheel(modifier = Modifier.fillMaxSize()) { color ->
                                        secondaryColorHex = color.toHexCode()
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Button(onClick = { showSecondaryColorPicker = false }, modifier = Modifier.fillMaxWidth()) {
                                    Text("Done")
                                }
                            }
                        }
                    }
"""

color_pickers_new = """
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = primaryColorHex, 
                            onValueChange = { primaryColorHex = it }, 
                            label = { Text("Primary Color") }, 
                            modifier = Modifier.weight(1f), 
                            singleLine = true,
                            leadingIcon = {
                                Box(modifier = Modifier.padding(start = 12.dp, end = 4.dp).size(24.dp).background(try { Color(android.graphics.Color.parseColor(primaryColorHex)) } catch (e: Exception) { Color.Transparent }, androidx.compose.foundation.shape.CircleShape))
                            },
                            trailingIcon = {
                                IconButton(onClick = { showPrimaryColorPicker = true }) {
                                    Icon(Icons.Default.Edit, contentDescription = "Pick Color")
                                }
                            }
                        )
                        OutlinedTextField(
                            value = secondaryColorHex, 
                            onValueChange = { secondaryColorHex = it }, 
                            label = { Text("Secondary Color") }, 
                            modifier = Modifier.weight(1f), 
                            singleLine = true,
                            leadingIcon = {
                                Box(modifier = Modifier.padding(start = 12.dp, end = 4.dp).size(24.dp).background(try { Color(android.graphics.Color.parseColor(secondaryColorHex)) } catch (e: Exception) { Color.Transparent }, androidx.compose.foundation.shape.CircleShape))
                            },
                            trailingIcon = {
                                IconButton(onClick = { showSecondaryColorPicker = true }) {
                                    Icon(Icons.Default.Edit, contentDescription = "Pick Color")
                                }
                            }
                        )
                    }
                    
                    if (showPrimaryColorPicker) {
                        var tempColorHex by remember { mutableStateOf(primaryColorHex) }
                        val oldColor = try { Color(android.graphics.Color.parseColor(primaryColorHex)) } catch(e: Exception) { Color.Transparent }
                        val newColor = try { Color(android.graphics.Color.parseColor(tempColorHex)) } catch(e: Exception) { Color.Transparent }
                        
                        Dialog(onDismissRequest = { showPrimaryColorPicker = false }) {
                            DarkCard(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Text("Select Primary Color", color = Color.White, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(16.dp))
                                Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
                                    ColorWheel(modifier = Modifier.fillMaxSize()) { color ->
                                        tempColorHex = color.toHexCode()
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                        Box(modifier = Modifier.size(40.dp).background(oldColor, androidx.compose.foundation.shape.CircleShape))
                                        Text("Before", color = Color.White, fontSize = 12.sp)
                                    }
                                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                        Box(modifier = Modifier.size(40.dp).background(newColor, androidx.compose.foundation.shape.CircleShape))
                                        Text("After", color = Color.White, fontSize = 12.sp)
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                                    TextButton(onClick = { showPrimaryColorPicker = false }) { Text("Cancel", color = Color.White) }
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Button(onClick = { primaryColorHex = tempColorHex; showPrimaryColorPicker = false }) { Text("Confirm") }
                                }
                            }
                        }
                    }
                    if (showSecondaryColorPicker) {
                        var tempColorHex by remember { mutableStateOf(secondaryColorHex) }
                        val oldColor = try { Color(android.graphics.Color.parseColor(secondaryColorHex)) } catch(e: Exception) { Color.Transparent }
                        val newColor = try { Color(android.graphics.Color.parseColor(tempColorHex)) } catch(e: Exception) { Color.Transparent }
                        
                        Dialog(onDismissRequest = { showSecondaryColorPicker = false }) {
                            DarkCard(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
                                Text("Select Secondary Color", color = Color.White, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(16.dp))
                                Box(modifier = Modifier.fillMaxWidth().aspectRatio(1f)) {
                                    ColorWheel(modifier = Modifier.fillMaxSize()) { color ->
                                        tempColorHex = color.toHexCode()
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly, verticalAlignment = Alignment.CenterVertically) {
                                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                        Box(modifier = Modifier.size(40.dp).background(oldColor, androidx.compose.foundation.shape.CircleShape))
                                        Text("Before", color = Color.White, fontSize = 12.sp)
                                    }
                                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                        Box(modifier = Modifier.size(40.dp).background(newColor, androidx.compose.foundation.shape.CircleShape))
                                        Text("After", color = Color.White, fontSize = 12.sp)
                                    }
                                }
                                Spacer(modifier = Modifier.height(16.dp))
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                                    TextButton(onClick = { showSecondaryColorPicker = false }) { Text("Cancel", color = Color.White) }
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Button(onClick = { secondaryColorHex = tempColorHex; showSecondaryColorPicker = false }) { Text("Confirm") }
                                }
                            }
                        }
                    }
"""

if "Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {" in content:
    content = content.replace(color_pickers_old.strip(), color_pickers_new.strip())
    with open("app/src/main/java/com/example/ui/screens/SettingsScreen.kt", "w") as f:
        f.write(content)
    print("Replaced!")
else:
    print("Failed!")
