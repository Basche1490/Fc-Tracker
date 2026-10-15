with open("app/src/main/java/com/example/ui/screens/MockDesignGalleryScreen.kt", "r") as f:
    text = f.read()

new_content = """package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun MockDesignGalleryScreen(onMenuClick: () -> Unit) {
    var selectedStyle by remember { mutableStateOf(0) }

    Column(modifier = Modifier.fillMaxSize().background(Color.White)) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onMenuClick) {
                Icon(Icons.Default.Menu, "Menu", tint = Color.Black)
            }
            Text("Minimalist Variations", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color.Black)
        }

        ScrollableTabRow(
            selectedTabIndex = selectedStyle,
            edgePadding = 16.dp,
            containerColor = Color.White,
            contentColor = Color.Black,
            divider = {}
        ) {
            val tabs = listOf("Electric Blue", "Warm Coral", "Stark Monochrome", "Fresh Mint", "Royal Violet", "Sunset Orange", "Navy & Gold")
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = selectedStyle == index,
                    onClick = { selectedStyle = index },
                    text = { Text(title, fontWeight = FontWeight.Bold) }
                )
            }
        }

        Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
            when (selectedStyle) {
                0 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFF2563EB), surfaceColor = Color(0xFFF8FAFC), textColor = Color(0xFF0F172A), mutedColor = Color(0xFF64748B), cornerRadius = 24
                )
                1 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFFF43F5E), surfaceColor = Color(0xFFFFF1F2), textColor = Color(0xFF4C0519), mutedColor = Color(0xFF9F1239), cornerRadius = 32
                )
                2 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFF000000), surfaceColor = Color(0xFFFFFFFF), textColor = Color(0xFF000000), mutedColor = Color(0xFF52525B), cornerRadius = 0, showBorders = true
                )
                3 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFF10B981), surfaceColor = Color(0xFFF0FDF4), textColor = Color(0xFF064E3B), mutedColor = Color(0xFF047857), cornerRadius = 16
                )
                4 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFF7C3AED), surfaceColor = Color(0xFFF5F3FF), textColor = Color(0xFF2E1065), mutedColor = Color(0xFF5B21B6), cornerRadius = 20
                )
                5 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFFEA580C), surfaceColor = Color(0xFFFFF7ED), textColor = Color(0xFF431407), mutedColor = Color(0xFF9A3412), cornerRadius = 12
                )
                6 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFFD97706), surfaceColor = Color(0xFFF1F5F9), textColor = Color(0xFF0F172A), mutedColor = Color(0xFF334155), cornerRadius = 8
                )
            }
        }
    }
}

@Composable
fun MinimalistThemeMockup(
    primaryColor: Color, surfaceColor: Color, textColor: Color, mutedColor: Color, cornerRadius: Int, showBorders: Boolean = false
) {
    val cardShape = RoundedCornerShape(cornerRadius.dp)
    val cardModifier = if (showBorders) {
        Modifier.fillMaxWidth().clip(cardShape).background(surfaceColor).border(2.dp, textColor, cardShape).padding(20.dp)
    } else {
        Modifier.fillMaxWidth().clip(cardShape).background(surfaceColor).padding(20.dp)
    }
    
    val smallCardModifier = if (showBorders) {
        Modifier.fillMaxWidth().clip(cardShape).background(surfaceColor).border(2.dp, textColor, cardShape).padding(16.dp)
    } else {
        Modifier.fillMaxWidth().clip(cardShape).background(surfaceColor).padding(16.dp)
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(Color.White).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(32.dp)
    ) {
        // --- 1. DASHBOARD SECTION ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("1. DASHBOARD", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column {
                        Text("Welcome back,", fontSize = 14.sp, color = mutedColor)
                        Text("Manager", fontSize = 28.sp, fontWeight = FontWeight.Black, color = textColor)
                    }
                    IconButton(onClick = {}, modifier = if(showBorders) Modifier.border(2.dp, textColor, CircleShape) else Modifier.background(surfaceColor, CircleShape)) {
                        Icon(Icons.Default.Notifications, contentDescription = null, tint = textColor)
                    }
                }
                
                Box(modifier = cardModifier) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                        Text("NEXT FIXTURE", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = primaryColor, letterSpacing = 2.sp)
                        Spacer(Modifier.height(16.dp))
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceEvenly, modifier = Modifier.fillMaxWidth()) {
                            Text("HOME", fontWeight = FontWeight.Black, color = textColor)
                            Text("vs", color = mutedColor)
                            Text("AWAY", fontWeight = FontWeight.Black, color = textColor)
                        }
                        Spacer(Modifier.height(16.dp))
                        Button(
                            onClick = {}, colors = ButtonDefaults.buttonColors(containerColor = primaryColor, contentColor = Color.White), 
                            shape = RoundedCornerShape(if(showBorders) 0.dp else 12.dp), modifier = Modifier.fillMaxWidth().height(48.dp)
                        ) {
                            Text("Match Center", fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }

        // --- 2. SQUAD SECTION ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("2. SQUAD LIST", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                
                Box(modifier = smallCardModifier) {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        listOf("ST" to "J. Doe" to "88", "CM" to "A. Smith" to "84", "CB" to "R. Johnson" to "86").forEach { (posName, ovr) ->
                            Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                                Box(modifier = Modifier.width(40.dp)) { Text(posName.first, fontWeight = FontWeight.Bold, color = primaryColor) }
                                Text(posName.second, modifier = Modifier.weight(1f), fontWeight = FontWeight.Medium, color = textColor)
                                Box(
                                    modifier = Modifier.clip(RoundedCornerShape(8.dp)).background(if(showBorders) Color.White else textColor.copy(alpha=0.1f)).then(if(showBorders) Modifier.border(1.dp, textColor, RoundedCornerShape(8.dp)) else Modifier).padding(horizontal = 8.dp, vertical = 4.dp)
                                ) {
                                    Text(ovr, fontWeight = FontWeight.Black, color = textColor, fontSize = 14.sp)
                                }
                            }
                            if (posName.second != "R. Johnson") {
                                HorizontalDivider(color = mutedColor.copy(alpha=0.2f))
                            }
                        }
                    }
                }
            }
        }
        
        // --- 3. TACTICS SECTION ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("3. TACTICS & FORMATION", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                
                Box(modifier = cardModifier.aspectRatio(0.8f), contentAlignment = Alignment.Center) {
                    Box(modifier = Modifier.fillMaxSize().border(2.dp, mutedColor.copy(alpha=0.3f), RoundedCornerShape(8.dp)))
                    Box(modifier = Modifier.fillMaxWidth().height(2.dp).background(mutedColor.copy(alpha=0.3f)))
                    Box(modifier = Modifier.size(60.dp).border(2.dp, mutedColor.copy(alpha=0.3f), CircleShape))
                    
                    Column(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.SpaceBetween, horizontalAlignment = Alignment.CenterHorizontally) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) { repeat(3) { TacticalDot(primaryColor, showBorders, textColor) } }
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) { repeat(3) { TacticalDot(primaryColor, showBorders, textColor) } }
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) { repeat(4) { TacticalDot(primaryColor, showBorders, textColor) } }
                        TacticalDot(primaryColor, showBorders, textColor)
                    }
                }
            }
        }
        
        // --- 4. MATCHES & FIXTURES ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("4. MATCHES & FIXTURES", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                Box(modifier = cardModifier) {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Oct 12", color = mutedColor, fontSize = 12.sp)
                            Text("2 - 1", fontWeight = FontWeight.Bold, color = primaryColor)
                        }
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Home Team", fontWeight = FontWeight.Medium, color = textColor)
                            Text("Away Team", fontWeight = FontWeight.Medium, color = mutedColor)
                        }
                    }
                }
            }
        }
        
        // --- 5. TRANSFERS ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("5. TRANSFERS", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                Box(modifier = cardModifier) {
                    Column {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(modifier = Modifier.size(48.dp).clip(CircleShape).background(primaryColor.copy(alpha=0.1f)), contentAlignment = Alignment.Center) {
                                Icon(Icons.Default.Person, contentDescription = null, tint = primaryColor)
                            }
                            Spacer(Modifier.width(12.dp))
                            Column {
                                Text("E. Haaland", fontWeight = FontWeight.Bold, color = textColor)
                                Text("ST • $120.0M", fontSize = 12.sp, color = mutedColor)
                            }
                        }
                        Spacer(Modifier.height(16.dp))
                        Button(onClick = {}, colors = ButtonDefaults.buttonColors(containerColor = if(showBorders) Color.White else surfaceColor, contentColor = primaryColor), border = androidx.compose.foundation.BorderStroke(if(showBorders) 2.dp else 1.dp, primaryColor), modifier = Modifier.fillMaxWidth()) {
                            Text("Make Offer", fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }

        // --- 6. YOUTH ACADEMY ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("6. YOUTH ACADEMY", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                Box(modifier = smallCardModifier) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                        Column {
                            Text("Scouted Prospect", fontWeight = FontWeight.Medium, color = textColor)
                            Text("15 yrs • Spain", fontSize = 12.sp, color = mutedColor)
                        }
                        Column(horizontalAlignment = Alignment.End) {
                            Text("Potential", fontSize = 10.sp, color = mutedColor)
                            Text("78 - 94", fontWeight = FontWeight.Black, color = primaryColor)
                        }
                    }
                }
            }
        }

        // --- 7. CLUB FINANCES ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("7. CLUB FINANCES", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                
                Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    Box(modifier = Modifier.weight(1f).aspectRatio(1.2f).then(smallCardModifier)) {
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                            Icon(Icons.Default.ShoppingCart, contentDescription = null, tint = primaryColor)
                            Column {
                                Text("Transfer", fontSize = 12.sp, color = mutedColor)
                                Text("$45M", fontSize = 24.sp, fontWeight = FontWeight.Black, color = textColor)
                            }
                        }
                    }
                    Box(modifier = Modifier.weight(1f).aspectRatio(1.2f).then(smallCardModifier)) {
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                            Icon(Icons.Default.Build, contentDescription = null, tint = primaryColor)
                            Column {
                                Text("Wages", fontSize = 12.sp, color = mutedColor)
                                Text("$1.2M", fontSize = 24.sp, fontWeight = FontWeight.Black, color = textColor)
                            }
                        }
                    }
                }
            }
        }
        
        // --- 8. SEASON SUMMARY ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("8. SEASON SUMMARY", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    Box(modifier = Modifier.weight(1f).aspectRatio(1.2f).then(smallCardModifier)) {
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                            Text("Goals\nScored", fontSize = 12.sp, color = mutedColor)
                            Text("84", fontSize = 28.sp, fontWeight = FontWeight.Black, color = textColor)
                        }
                    }
                    Box(modifier = Modifier.weight(1f).aspectRatio(1.2f).then(smallCardModifier)) {
                        Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                            Text("Clean\nSheets", fontSize = 12.sp, color = mutedColor)
                            Text("15", fontSize = 28.sp, fontWeight = FontWeight.Black, color = textColor)
                        }
                    }
                }
            }
        }

        // --- 9. CAREER SUMMARY ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("9. CAREER SUMMARY", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                Box(modifier = cardModifier) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                        Icon(Icons.Default.Star, contentDescription = null, tint = primaryColor, modifier = Modifier.size(48.dp))
                        Spacer(Modifier.height(8.dp))
                        Text("Hall of Fame", fontWeight = FontWeight.Bold, color = textColor)
                        Text("3x League Titles, 1x Cup", fontSize = 12.sp, color = mutedColor)
                    }
                }
            }
        }

        // --- 10. AI ASSISTANT ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("10. AI ASSISTANT", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                Box(modifier = cardModifier) {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Box(modifier = Modifier.align(Alignment.End).clip(RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp, bottomStart = 16.dp, bottomEnd = 0.dp)).background(primaryColor).padding(12.dp)) {
                            Text("Suggest a training focus.", color = Color.White, fontSize = 14.sp)
                        }
                        Box(modifier = Modifier.align(Alignment.Start).clip(RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp, bottomStart = 0.dp, bottomEnd = 16.dp)).background(if(showBorders) Color.White else textColor.copy(alpha=0.05f)).then(if(showBorders) Modifier.border(2.dp, textColor, RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp, bottomStart = 0.dp, bottomEnd = 16.dp)) else Modifier).padding(12.dp)) {
                            Text("Focus on Attacking. Next opponent is weak on the wings.", color = textColor, fontSize = 14.sp)
                        }
                    }
                }
            }
        }

        // --- 11. SETTINGS ---
        item {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Text("11. SETTINGS", fontSize = 12.sp, fontWeight = FontWeight.Black, color = mutedColor, letterSpacing = 2.sp)
                Box(modifier = cardModifier) {
                    Column {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Notifications", color = textColor, fontWeight = FontWeight.Medium)
                            Switch(checked = true, onCheckedChange = {}, colors = SwitchDefaults.colors(checkedThumbColor = Color.White, checkedTrackColor = primaryColor, uncheckedBorderColor = textColor, uncheckedThumbColor = mutedColor))
                        }
                        HorizontalDivider(modifier = Modifier.padding(vertical = 12.dp), color = mutedColor.copy(alpha=0.2f))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Currency", color = textColor, fontWeight = FontWeight.Medium)
                            Text("USD ($)", color = mutedColor)
                        }
                    }
                }
            }
        }
        
        item { Spacer(Modifier.height(40.dp)) }
    }
}

@Composable
fun TacticalDot(color: Color, showBorders: Boolean, textColor: Color) {
    Box(
        modifier = Modifier.size(16.dp).clip(CircleShape).background(if(showBorders) Color.White else color).then(if(showBorders) Modifier.border(2.dp, textColor, CircleShape) else Modifier)
    )
}
"""

with open("app/src/main/java/com/example/ui/screens/MockDesignGalleryScreen.kt", "w") as f:
    f.write(new_content)
