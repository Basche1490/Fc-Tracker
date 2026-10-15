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
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.SportsSoccer
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
            Text("Modern Minimalist Options", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color.Black)
        }

        ScrollableTabRow(
            selectedTabIndex = selectedStyle,
            edgePadding = 16.dp,
            containerColor = Color.White,
            contentColor = Color.Black,
            divider = {}
        ) {
            val tabs = listOf("Electric Blue", "Warm Coral", "Stark Monochrome", "Fresh Mint")
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
                    primaryColor = Color(0xFF2563EB), // Electric Blue
                    surfaceColor = Color(0xFFF8FAFC),
                    textColor = Color(0xFF0F172A),
                    mutedColor = Color(0xFF64748B),
                    cornerRadius = 24
                )
                1 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFFF43F5E), // Warm Coral
                    surfaceColor = Color(0xFFFFF1F2),
                    textColor = Color(0xFF4C0519),
                    mutedColor = Color(0xFF9F1239),
                    cornerRadius = 32
                )
                2 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFF000000), // Stark Monochrome
                    surfaceColor = Color(0xFFFFFFFF),
                    textColor = Color(0xFF000000),
                    mutedColor = Color(0xFF52525B),
                    cornerRadius = 0,
                    showBorders = true
                )
                3 -> MinimalistThemeMockup(
                    primaryColor = Color(0xFF10B981), // Fresh Mint
                    surfaceColor = Color(0xFFF0FDF4),
                    textColor = Color(0xFF064E3B),
                    mutedColor = Color(0xFF047857),
                    cornerRadius = 16
                )
            }
        }
    }
}

@Composable
fun MinimalistThemeMockup(
    primaryColor: Color,
    surfaceColor: Color,
    textColor: Color,
    mutedColor: Color,
    cornerRadius: Int,
    showBorders: Boolean = false
) {
    val cardShape = RoundedCornerShape(cornerRadius.dp)
    val cardModifier = if (showBorders) {
        Modifier.fillMaxWidth().clip(cardShape).background(surfaceColor).border(2.dp, textColor, cardShape).padding(20.dp)
    } else {
        Modifier.fillMaxWidth().clip(cardShape).background(surfaceColor).padding(20.dp)
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(Color.White).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        item {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Column {
                    Text("Welcome back,", fontSize = 14.sp, color = mutedColor)
                    Text("Manager", fontSize = 28.sp, fontWeight = FontWeight.Black, color = textColor)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    IconButton(onClick = {}, modifier = if(showBorders) Modifier.border(2.dp, textColor, CircleShape) else Modifier.background(surfaceColor, CircleShape)) {
                        Icon(Icons.Default.Search, contentDescription = null, tint = textColor)
                    }
                    IconButton(onClick = {}, modifier = if(showBorders) Modifier.border(2.dp, textColor, CircleShape) else Modifier.background(surfaceColor, CircleShape)) {
                        Icon(Icons.Default.Notifications, contentDescription = null, tint = textColor)
                    }
                }
            }
        }

        item {
            Box(modifier = cardModifier) {
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    Text("NEXT FIXTURE", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = primaryColor, letterSpacing = 2.sp)
                    Spacer(Modifier.height(24.dp))
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center, modifier = Modifier.fillMaxWidth()) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Box(modifier = Modifier.size(64.dp).clip(CircleShape).background(if(showBorders) Color.White else Color.White).border(if(showBorders) 2.dp else 0.dp, textColor, CircleShape), contentAlignment = Alignment.Center) {
                                Text("HM", fontWeight = FontWeight.Black, color = textColor)
                            }
                            Spacer(Modifier.height(8.dp))
                            Text("Home Team", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = textColor)
                        }
                        
                        Text("  vs  ", fontSize = 16.sp, color = mutedColor, fontWeight = FontWeight.Medium, modifier = Modifier.padding(horizontal = 16.dp).padding(bottom = 24.dp))
                        
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Box(modifier = Modifier.size(64.dp).clip(CircleShape).background(if(showBorders) Color.White else Color.White).border(if(showBorders) 2.dp else 0.dp, textColor, CircleShape), contentAlignment = Alignment.Center) {
                                Text("AW", fontWeight = FontWeight.Black, color = textColor)
                            }
                            Spacer(Modifier.height(8.dp))
                            Text("Away Team", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = textColor)
                        }
                    }
                    Spacer(Modifier.height(24.dp))
                    Button(
                        onClick = {}, 
                        colors = ButtonDefaults.buttonColors(containerColor = primaryColor, contentColor = Color.White), 
                        shape = RoundedCornerShape(if(showBorders) 0.dp else 12.dp),
                        modifier = Modifier.fillMaxWidth().height(50.dp)
                    ) {
                        Text("Match Center", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    }
                }
            }
        }

        item {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                Box(modifier = Modifier.weight(1f).aspectRatio(1f).clip(cardShape).background(surfaceColor).then(if(showBorders) Modifier.border(2.dp, textColor, cardShape) else Modifier).padding(16.dp)) {
                    Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                        Icon(Icons.Default.SportsSoccer, contentDescription = null, tint = primaryColor, modifier = Modifier.size(32.dp))
                        Column {
                            Text("League Pos", fontSize = 12.sp, color = mutedColor)
                            Text("1st", fontSize = 36.sp, fontWeight = FontWeight.Black, color = textColor)
                        }
                    }
                }
                Box(modifier = Modifier.weight(1f).aspectRatio(1f).clip(cardShape).background(surfaceColor).then(if(showBorders) Modifier.border(2.dp, textColor, cardShape) else Modifier).padding(16.dp)) {
                    Column(modifier = Modifier.fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                            repeat(5) { 
                                val dotColor = if(it < 4) primaryColor else mutedColor.copy(alpha=0.3f)
                                Box(modifier = Modifier.size(12.dp).clip(if(showBorders) RoundedCornerShape(0.dp) else CircleShape).background(dotColor).then(if(showBorders) Modifier.border(1.dp, textColor) else Modifier)) 
                            }
                        }
                        Column {
                            Text("Form", fontSize = 12.sp, color = mutedColor)
                            Text("W W W W D", fontSize = 20.sp, fontWeight = FontWeight.Black, color = textColor)
                        }
                    }
                }
            }
        }
    }
}
"""

with open("app/src/main/java/com/example/ui/screens/MockDesignGalleryScreen.kt", "w") as f:
    f.write(new_content)
