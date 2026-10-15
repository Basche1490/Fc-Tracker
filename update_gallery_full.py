with open("app/src/main/java/com/example/ui/screens/MockDesignGalleryScreen.kt", "r") as f:
    text = f.read()

import re

# We will completely replace the contents of the MockDesignGalleryScreen.kt
new_content = """package com.example.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.R

@Composable
fun MockDesignGalleryScreen(onMenuClick: () -> Unit) {
    var selectedStyle by remember { mutableStateOf(0) }

    Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        Row(
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onMenuClick) {
                Icon(Icons.Default.Menu, "Menu", tint = MaterialTheme.colorScheme.primary)
            }
            Text("Design Gallery", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
        }

        ScrollableTabRow(
            selectedTabIndex = selectedStyle,
            edgePadding = 16.dp,
            containerColor = Color.Transparent,
            divider = {}
        ) {
            val tabs = listOf("Modern Minimalist", "High-Tech Tactical", "Executive Premium", "Retro 90s", "Vibrant Glassmorphism", "Neumorphic Soft", "Cyberpunk Synthwave")
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = selectedStyle == index,
                    onClick = { selectedStyle = index },
                    text = { Text(title, fontWeight = FontWeight.Bold) }
                )
            }
        }

        Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
            val imageResList = when (selectedStyle) {
                0 -> listOf(R.drawable.mockup_modern, R.drawable.mockup_modern_squad)
                1 -> listOf(R.drawable.mockup_tactical)
                2 -> listOf(R.drawable.mockup_executive, R.drawable.mockup_executive_finance)
                3 -> listOf(R.drawable.mockup_retro, R.drawable.mockup_retro_match)
                4 -> listOf(R.drawable.mockup_glass, R.drawable.mockup_glass_inbox)
                5 -> listOf(R.drawable.mockup_neumorphic_dash, R.drawable.mockup_neumorphic_squad)
                6 -> listOf(R.drawable.mockup_cyberpunk_dash, R.drawable.mockup_cyberpunk_transfers)
                else -> listOf(R.drawable.mockup_modern)
            }
            
            LazyColumn(modifier = Modifier.fillMaxSize()) {
                items(imageResList) { imageRes ->
                    Image(
                        painter = painterResource(id = imageRes),
                        contentDescription = "Design Mockup",
                        modifier = Modifier.fillMaxWidth().aspectRatio(0.46f).padding(16.dp), // Approx standard mobile aspect ratio to let it scroll
                        contentScale = ContentScale.Fit
                    )
                }
            }
        }
    }
}
"""

with open("app/src/main/java/com/example/ui/screens/MockDesignGalleryScreen.kt", "w") as f:
    f.write(new_content)
