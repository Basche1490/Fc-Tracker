package com.example.ui.screens

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowForwardIos
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun MockDesignGalleryScreen(onMenuClick: () -> Unit) {
    var selectedStyle by remember { mutableStateOf(0) }

    val styles = listOf(
        "1. Bento Modular Grid",
        "2. Apple Inset & Segmented",
        "3. App Icon Studio"
    )

    Column(modifier = Modifier.fillMaxSize().background(Color(0xFFF9FAFB))) {
        // Top Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color.White)
                .padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onClick = onMenuClick) {
                Icon(Icons.Default.Menu, "Menu", tint = Color(0xFF111827))
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    "UI Architecture & Icon Lab",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF111827)
                )
                Text(
                    "Explore Bento Modular, Apple Inset & App Icon Concepts",
                    fontSize = 12.sp,
                    color = Color(0xFF6B7280)
                )
            }
        }

        // Segmented Tab Row for the Styles + App Icon Studio
        ScrollableTabRow(
            selectedTabIndex = selectedStyle,
            edgePadding = 16.dp,
            containerColor = Color.White,
            contentColor = Color(0xFF111827),
            divider = { HorizontalDivider(color = Color(0xFFE5E7EB)) }
        ) {
            styles.forEachIndexed { index, title ->
                Tab(
                    selected = selectedStyle == index,
                    onClick = { selectedStyle = index },
                    text = {
                        Text(
                            title,
                            fontWeight = if (selectedStyle == index) FontWeight.Bold else FontWeight.Medium,
                            fontSize = 13.sp,
                            color = if (selectedStyle == index) Color(0xFF1D4ED8) else Color(0xFF6B7280)
                        )
                    }
                )
            }
        }

        // Active UI Style Preview
        Box(modifier = Modifier.weight(1f).fillMaxWidth()) {
            when (selectedStyle) {
                0 -> BentoModularStyleMockup()
                1 -> AppleInsetSegmentedStyleMockup()
                2 -> AppIconStudioMockup()
            }
        }
    }
}

// =========================================================================
// STYLE 1: BENTO MODULAR GRID
// Multi-page architectural preview covering Dashboard, Squad, Matches,
// Transfers, Youth Academy, and Career Trophy Cabinet.
// =========================================================================
@Composable
fun BentoModularStyleMockup() {
    val bg = Color(0xFFF3F4F6)
    val cardBg = Color.White
    val accent = Color(0xFF2563EB)
    val textPrimary = Color(0xFF111827)
    val textSecondary = Color(0xFF6B7280)

    var selectedSection by remember { mutableStateOf(0) }
    val sections = listOf(
        "All Sections",
        "Dashboard",
        "Squad & Pitch",
        "Matches & Center",
        "Transfer Hub",
        "Youth Academy",
        "Career Cabinet"
    )

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(bg).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        item {
            DesignExplainerHeader(
                name = "Bento Modular Grid",
                corePhilosophy = "Asymmetrical tiles, embedded status chips, modular stat grouping, and radial progress rings. Every screen follows a cohesive, grid-based dashboard language.",
                keyElements = listOf("Asymmetric Bento Boxes", "Corner Status Chips", "Live Telemetry Tiles", "Radial Metric Rings")
            )
        }

        // Section Filter Chips
        item {
            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                itemsIndexed(sections) { index, title ->
                    val isSelected = selectedSection == index
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(20.dp))
                            .background(if (isSelected) accent else Color.White)
                            .border(1.dp, if (isSelected) accent else Color(0xFFE5E7EB), RoundedCornerShape(20.dp))
                            .clickable { selectedSection = index }
                            .padding(horizontal = 14.dp, vertical = 7.dp)
                    ) {
                        Text(
                            title,
                            fontSize = 12.sp,
                            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                            color = if (isSelected) Color.White else textPrimary
                        )
                    }
                }
            }
        }

        // =================================================================
        // 1. DASHBOARD BENTO TILES
        // =================================================================
        if (selectedSection == 0 || selectedSection == 1) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("01 // DASHBOARD & MATCHDAY HUB", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                    // Hero Matchday Bento Tile
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(24.dp))
                            .background(cardBg)
                            .padding(20.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(accent.copy(alpha = 0.1f))
                                        .padding(horizontal = 10.dp, vertical = 4.dp)
                                ) {
                                    Text("MATCHDAY 18", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = accent)
                                }
                                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                    Box(modifier = Modifier.size(8.dp).clip(CircleShape).background(Color(0xFF10B981)))
                                    Text("Live Sync Ready", fontSize = 11.sp, color = textSecondary, fontWeight = FontWeight.Medium)
                                }
                            }

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceAround,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    Box(
                                        modifier = Modifier.size(52.dp).clip(CircleShape).background(Color(0xFFEFF6FF)),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text("RIC", fontWeight = FontWeight.Black, color = accent)
                                    }
                                    Spacer(Modifier.height(6.dp))
                                    Text("Richmond", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                    Text("1st • 41 pts", fontSize = 11.sp, color = textSecondary)
                                }

                                Box(
                                    modifier = Modifier
                                        .clip(CircleShape)
                                        .background(Color(0xFFF3F4F6))
                                        .padding(horizontal = 14.dp, vertical = 6.dp)
                                ) {
                                    Text("VS", fontWeight = FontWeight.Black, fontSize = 12.sp, color = textPrimary)
                                }

                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    Box(
                                        modifier = Modifier.size(52.dp).clip(CircleShape).background(Color(0xFFFEE2E2)),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text("ARS", fontWeight = FontWeight.Black, color = Color(0xFFDC2626))
                                    }
                                    Spacer(Modifier.height(6.dp))
                                    Text("Arsenal", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                    Text("2nd • 39 pts", fontSize = 11.sp, color = textSecondary)
                                }
                            }

                            Button(
                                onClick = {},
                                shape = RoundedCornerShape(16.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = accent),
                                modifier = Modifier.fillMaxWidth().height(46.dp)
                            ) {
                                Text("Enter Match Center", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            }
                        }
                    }

                    // 2-Column Split Bento: Form & Morale
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(20.dp))
                                .background(cardBg)
                                .padding(16.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                                Text("RECENT FORM", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    listOf("W", "W", "W", "D", "W").forEach { result ->
                                        Box(
                                            modifier = Modifier
                                                .size(24.dp)
                                                .clip(CircleShape)
                                                .background(if (result == "W") Color(0xFF10B981) else Color(0xFFF59E0B)),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text(result, color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                }
                                Text("13 pts from 15", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textPrimary)
                            }
                        }

                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(20.dp))
                                .background(cardBg)
                                .padding(16.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                Text("SQUAD MORALE", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Text("94%", fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color(0xFF10B981))
                                Text("High dressing room trust", fontSize = 11.sp, color = textSecondary)
                            }
                        }
                    }

                    // Telemetry Sync Status Tile
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(18.dp))
                            .background(Color(0xFF0F172A))
                            .padding(14.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                                Box(
                                    modifier = Modifier.size(36.dp).clip(CircleShape).background(Color(0xFF1E293B)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.Sync, contentDescription = null, tint = Color(0xFF38BDF8), modifier = Modifier.size(18.dp))
                                }
                                Column {
                                    Text("LIVE TELEMETRY BRIDGE", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                    Text("Auto-syncing matches & transfers • Port 8080", fontSize = 10.sp, color = Color(0xFF94A3B8))
                                }
                            }
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(6.dp))
                                    .background(Color(0xFF10B981).copy(alpha = 0.2f))
                                    .padding(horizontal = 8.dp, vertical = 3.dp)
                            ) {
                                Text("CONNECTED", fontSize = 10.sp, fontWeight = FontWeight.Black, color = Color(0xFF10B981))
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 2. SQUAD & PITCH BENTO TILES
        // =================================================================
        if (selectedSection == 0 || selectedSection == 2) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("02 // SQUAD, FORMATION & TACTICAL PITCH", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                    // Tactical Pitch Bento Box
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(24.dp))
                            .background(Color(0xFF0F172A))
                            .padding(20.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Column {
                                    Text("TACTICAL SYSTEM", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color(0xFF94A3B8), letterSpacing = 1.sp)
                                    Text("4-3-3 Attack (Fluid Tiki-Taka)", fontWeight = FontWeight.Black, color = Color.White, fontSize = 16.sp)
                                }
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(Color(0xFF1E293B))
                                        .padding(horizontal = 10.dp, vertical = 4.dp)
                                ) {
                                    Text("HIGH PRESS", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF38BDF8))
                                }
                            }

                            // Chalkboard pitch representation
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(140.dp)
                                    .clip(RoundedCornerShape(16.dp))
                                    .background(Color(0xFF1E293B))
                                    .border(1.dp, Color(0xFF334155), RoundedCornerShape(16.dp)),
                                contentAlignment = Alignment.Center
                            ) {
                                Column(
                                    modifier = Modifier.fillMaxSize().padding(14.dp),
                                    verticalArrangement = Arrangement.SpaceBetween,
                                    horizontalAlignment = Alignment.CenterHorizontally
                                ) {
                                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                                        TacticalNode("9", Color(0xFF38BDF8))
                                        TacticalNode("10", Color(0xFF38BDF8))
                                        TacticalNode("11", Color(0xFF38BDF8))
                                    }
                                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                                        TacticalNode("8", Color(0xFF818CF8))
                                        TacticalNode("4", Color(0xFF818CF8))
                                        TacticalNode("6", Color(0xFF818CF8))
                                    }
                                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                                        TacticalNode("2", Color(0xFF94A3B8))
                                        TacticalNode("5", Color(0xFF94A3B8))
                                        TacticalNode("3", Color(0xFF94A3B8))
                                        TacticalNode("1", Color(0xFFF59E0B))
                                    }
                                }
                            }
                        }
                    }

                    // Modular Player Roster Cards
                    listOf(
                        Triple("Jamie Tartt", "ST", Pair("88", "Superb Form")),
                        Triple("Dani Rojas", "LW", Pair("84", "High Morale")),
                        Triple("Isaac McAdoo", "CB", Pair("86", "Captain"))
                    ).forEach { (name, pos, data) ->
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(18.dp))
                                .background(cardBg)
                                .padding(14.dp)
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                    Box(
                                        modifier = Modifier
                                            .size(42.dp)
                                            .clip(RoundedCornerShape(12.dp))
                                            .background(accent.copy(alpha = 0.1f)),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text(data.first, fontWeight = FontWeight.Black, color = accent, fontSize = 16.sp)
                                    }
                                    Column {
                                        Text(name, fontWeight = FontWeight.Bold, fontSize = 14.sp, color = textPrimary)
                                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                                            Box(
                                                modifier = Modifier
                                                    .clip(RoundedCornerShape(4.dp))
                                                    .background(Color(0xFFE5E7EB))
                                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                                            ) {
                                                Text(pos, fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textPrimary)
                                            }
                                            Text(data.second, fontSize = 11.sp, color = textSecondary)
                                        }
                                    }
                                }
                                Icon(Icons.AutoMirrored.Filled.ArrowForwardIos, contentDescription = null, tint = textSecondary, modifier = Modifier.size(14.dp))
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 3. MATCHES & RESULTS BENTO TILES
        // =================================================================
        if (selectedSection == 0 || selectedSection == 3) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("03 // MATCHES, RESULTS & ANALYTICS MATRIX", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                    // Recent Match Center Bento Tile
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(22.dp))
                            .background(cardBg)
                            .padding(18.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Text("LATEST RESULT // FT", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(6.dp))
                                        .background(Color(0xFF10B981))
                                        .padding(horizontal = 8.dp, vertical = 3.dp)
                                ) {
                                    Text("WIN (+3 PTS)", fontSize = 10.sp, fontWeight = FontWeight.Black, color = Color.White)
                                }
                            }

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("Richmond FC", fontSize = 17.sp, fontWeight = FontWeight.Black, color = textPrimary)
                                Text("3 - 1", fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color(0xFF10B981))
                                Text("Arsenal FC", fontSize = 17.sp, fontWeight = FontWeight.Black, color = textPrimary)
                            }

                            HorizontalDivider(color = Color(0xFFF3F4F6))

                            // Scorers Row
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Tartt 24', 68' • Rojas 52'", fontSize = 11.sp, color = textSecondary, fontWeight = FontWeight.Medium)
                                Text("Saka 41'", fontSize = 11.sp, color = textSecondary, fontWeight = FontWeight.Medium)
                            }
                        }
                    }

                    // Analytics Split Tiles: xG & MOTM
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(20.dp))
                                .background(cardBg)
                                .padding(16.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                Text("EXPECTED GOALS (xG)", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Text("2.4 vs 0.9", fontSize = 20.sp, fontWeight = FontWeight.Black, color = textPrimary)
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .height(6.dp)
                                        .clip(CircleShape)
                                        .background(Color(0xFFE5E7EB))
                                ) {
                                    Box(
                                        modifier = Modifier
                                            .fillMaxHeight()
                                            .fillMaxWidth(0.72f)
                                            .clip(CircleShape)
                                            .background(Color(0xFF10B981))
                                    )
                                }
                            }
                        }

                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(20.dp))
                                .background(Color(0xFFFEF3C7))
                                .padding(16.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                Text("MAN OF THE MATCH", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color(0xFFB45309))
                                Text("Jamie Tartt", fontSize = 16.sp, fontWeight = FontWeight.Black, color = Color(0xFF78350F))
                                Text("Rating 9.4 • 2 Goals", fontSize = 11.sp, color = Color(0xFF92400E), fontWeight = FontWeight.Medium)
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 4. TRANSFERS & MARKET BENTO TILES
        // =================================================================
        if (selectedSection == 0 || selectedSection == 4) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("04 // TRANSFER HUB & BUDGET MATRIX", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(20.dp))
                                .background(cardBg)
                                .padding(16.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                Box(
                                    modifier = Modifier.size(32.dp).clip(CircleShape).background(Color(0xFFEFF6FF)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.AccountBalanceWallet, null, tint = accent, modifier = Modifier.size(16.dp))
                                }
                                Text("TRANSFER BUDGET", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Text("€85.0M", fontSize = 20.sp, fontWeight = FontWeight.Black, color = textPrimary)
                                Text("€12.5M allocated", fontSize = 11.sp, color = Color(0xFF10B981))
                            }
                        }

                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(20.dp))
                                .background(cardBg)
                                .padding(16.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                Box(
                                    modifier = Modifier.size(32.dp).clip(CircleShape).background(Color(0xFFFEF3C7)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Default.Payments, null, tint = Color(0xFFD97706), modifier = Modifier.size(16.dp))
                                }
                                Text("WAGE SPEND / WK", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Text("€1.42M", fontSize = 20.sp, fontWeight = FontWeight.Black, color = textPrimary)
                                Text("78% of cap", fontSize = 11.sp, color = textSecondary)
                            }
                        }
                    }

                    // Transfer Target Spotlight Card
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(20.dp))
                            .background(cardBg)
                            .padding(16.dp)
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                    Text("Lucas Paquetá", fontWeight = FontWeight.Bold, fontSize = 15.sp, color = textPrimary)
                                    Box(
                                        modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(Color(0xFFDCFCE7)).padding(horizontal = 6.dp, vertical = 2.dp)
                                    ) {
                                        Text("SCOUTED 95%", fontSize = 9.sp, fontWeight = FontWeight.Bold, color = Color(0xFF166534))
                                    }
                                }
                                Text("AM // West Ham • Est. €45.0M • Rel. Clause €65.0M", fontSize = 11.sp, color = textSecondary)
                            }
                            Button(
                                onClick = {},
                                shape = RoundedCornerShape(10.dp),
                                contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = accent)
                            ) {
                                Text("Bid", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 5. YOUTH ACADEMY BENTO TILES
        // =================================================================
        if (selectedSection == 0 || selectedSection == 5) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("05 // YOUTH ACADEMY & GLOBAL SCOUTING", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                    // Wonderkid Hero Spotlight Bento
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(22.dp))
                            .background(Color(0xFF1E1B4B)) // Indigo dark
                            .padding(18.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(Color(0xFF4338CA))
                                        .padding(horizontal = 10.dp, vertical = 4.dp)
                                ) {
                                    Text("WONDERKID PROSPECT", fontSize = 10.sp, fontWeight = FontWeight.Black, color = Color(0xFFA5B4FC))
                                }
                                Text("Scout Grade: A+", fontSize = 11.sp, color = Color(0xFFC7D2FE), fontWeight = FontWeight.Bold)
                            }

                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column {
                                    Text("Mateo Silva", fontSize = 18.sp, fontWeight = FontWeight.Black, color = Color.White)
                                    Text("16 yo • CAM • Brazil • 5★ Weak Foot", fontSize = 11.sp, color = Color(0xFFCBD5E1))
                                }
                                Column(horizontalAlignment = Alignment.End) {
                                    Text("POTENTIAL", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color(0xFFA5B4FC))
                                    Text("88 - 94", fontSize = 22.sp, fontWeight = FontWeight.Black, color = Color(0xFF38BDF8))
                                }
                            }

                            // Progress indicator
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(6.dp)
                                    .clip(CircleShape)
                                    .background(Color(0xFF312E81))
                            ) {
                                Box(
                                    modifier = Modifier
                                        .fillMaxHeight()
                                        .fillMaxWidth(0.91f)
                                        .clip(CircleShape)
                                        .background(Color(0xFF38BDF8))
                                )
                            }
                        }
                    }

                    // Scout Missions Split
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(18.dp))
                                .background(cardBg)
                                .padding(14.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                Text("SCOUT MISSION #1", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Text("Brazil (Technically Gifted)", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = textPrimary)
                                Text("12 days remaining • 6 found", fontSize = 10.sp, color = Color(0xFF10B981))
                            }
                        }
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(18.dp))
                                .background(cardBg)
                                .padding(14.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                Text("SCOUT MISSION #2", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Text("Spain (Playmakers)", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = textPrimary)
                                Text("24 days remaining • 4 found", fontSize = 10.sp, color = textSecondary)
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 6. CAREER CABINET BENTO TILES
        // =================================================================
        if (selectedSection == 0 || selectedSection == 6) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("06 // CAREER SUMMARY & TROPHY CABINET", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                    // Trophy Shelf Bento Tile
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(22.dp))
                            .background(cardBg)
                            .padding(18.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Text("SILVERWARE & HONOURS", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                listOf(
                                    Pair("Premier League", "2024/25"),
                                    Pair("Champions Cup", "2025/26"),
                                    Pair("FA Cup", "2024/25")
                                ).forEach { (trophy, season) ->
                                    Column(
                                        horizontalAlignment = Alignment.CenterHorizontally,
                                        modifier = Modifier.weight(1f)
                                    ) {
                                        Box(
                                            modifier = Modifier.size(44.dp).clip(CircleShape).background(Color(0xFFFEF3C7)),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Icon(Icons.Default.EmojiEvents, contentDescription = null, tint = Color(0xFFD97706), modifier = Modifier.size(22.dp))
                                        }
                                        Spacer(Modifier.height(6.dp))
                                        Text(trophy, fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textPrimary, textAlign = TextAlign.Center)
                                        Text(season, fontSize = 10.sp, color = textSecondary)
                                    }
                                }
                            }
                        }
                    }

                    // Lifetime Stats Split
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(18.dp))
                                .background(cardBg)
                                .padding(14.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                                Text("LIFETIME MATCHES", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Text("142", fontSize = 24.sp, fontWeight = FontWeight.Black, color = textPrimary)
                                Text("97W • 24D • 21L", fontSize = 10.sp, color = textSecondary)
                            }
                        }

                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(18.dp))
                                .background(cardBg)
                                .padding(14.dp)
                        ) {
                            Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                                Text("CAREER WIN RATE", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                                Text("68.3%", fontSize = 24.sp, fontWeight = FontWeight.Black, color = Color(0xFF10B981))
                                Text("Elite Manager Tier", fontSize = 10.sp, color = Color(0xFF10B981))
                            }
                        }
                    }
                }
            }
        }

        item { Spacer(Modifier.height(30.dp)) }
    }
}

// =========================================================================
// STYLE 2: APPLE INSET & SEGMENTED (iOS Native Sports Feel)
// Edge-to-edge grouped rows, hairline dividers, segmented pills, micro-chips
// Multi-page architectural preview covering Dashboard, Squad, Matches,
// Transfers, Youth Academy, and Career Trophy Cabinet.
// =========================================================================
@Composable
fun AppleInsetSegmentedStyleMockup() {
    val bg = Color(0xFFF2F2F7) // iOS system background
    val cardBg = Color.White
    val textPrimary = Color(0xFF000000)
    val textSecondary = Color(0xFF8E8E93)
    val appleBlue = Color(0xFF007AFF)

    var selectedSection by remember { mutableStateOf(0) }
    val sections = listOf(
        "All Sections",
        "Dashboard",
        "Squad & Pitch",
        "Matches & Center",
        "Transfer Hub",
        "Youth Academy",
        "Career Cabinet"
    )

    var dashboardSegment by remember { mutableStateOf(0) }

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(bg).padding(horizontal = 16.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(22.dp)
    ) {
        item {
            DesignExplainerHeader(
                name = "Apple Inset & Segmented",
                corePhilosophy = "Cardless grouped rows, 0.5dp hairline dividers, inline segmented switches, and generous typographic hierarchy across all app sections.",
                keyElements = listOf("Hairline Separators (0.5dp)", "Inset Grouped Lists", "Segmented Header Switches", "Micro SF-Style Pills")
            )
        }

        // Section Filter Chips
        item {
            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.fillMaxWidth()
            ) {
                itemsIndexed(sections) { index, title ->
                    val isSelected = selectedSection == index
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(20.dp))
                            .background(if (isSelected) appleBlue else Color.White)
                            .border(0.5.dp, if (isSelected) appleBlue else Color(0xFFD1D1D6), RoundedCornerShape(20.dp))
                            .clickable { selectedSection = index }
                            .padding(horizontal = 14.dp, vertical = 7.dp)
                    ) {
                        Text(
                            title,
                            fontSize = 12.sp,
                            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                            color = if (isSelected) Color.White else textPrimary
                        )
                    }
                }
            }
        }

        // =================================================================
        // 1. DASHBOARD INSET GROUP
        // =================================================================
        if (selectedSection == 0 || selectedSection == 1) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("01 // UPCOMING FIXTURE & CLUB OVERVIEW", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(cardBg)
                    ) {
                        Column {
                            // Segmented Switch inside
                            Box(modifier = Modifier.padding(12.dp)) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(Color(0xFFE5E5EA))
                                        .padding(2.dp)
                                ) {
                                    listOf("Matchday", "Table", "Scouting").forEachIndexed { i, title ->
                                        Box(
                                            modifier = Modifier
                                                .weight(1f)
                                                .clip(RoundedCornerShape(6.dp))
                                                .background(if (dashboardSegment == i) Color.White else Color.Transparent)
                                                .clickable { dashboardSegment = i }
                                                .padding(vertical = 6.dp),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text(
                                                title,
                                                fontSize = 12.sp,
                                                fontWeight = if (dashboardSegment == i) FontWeight.Bold else FontWeight.Normal,
                                                color = if (dashboardSegment == i) textPrimary else textSecondary
                                            )
                                        }
                                    }
                                }
                            }

                            HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp)

                            // Match Row
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 14.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Column {
                                    Text("Premier League • Round 18", fontSize = 11.sp, color = textSecondary)
                                    Spacer(Modifier.height(4.dp))
                                    Text("Richmond vs Arsenal", fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = textPrimary)
                                }
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(12.dp))
                                        .background(appleBlue)
                                        .padding(horizontal = 14.dp, vertical = 6.dp)
                                ) {
                                    Text("15:00", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                                }
                            }
                        }
                    }

                    // Key-Value Settings Rows
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(cardBg)
                    ) {
                        Column {
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("Telemetry Sync Engine", fontSize = 14.sp, color = textPrimary)
                                Text("Connected (Port 8080)", fontSize = 14.sp, color = Color(0xFF34C759), fontWeight = FontWeight.SemiBold)
                            }
                            HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp, modifier = Modifier.padding(start = 16.dp))
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("Board Objective Approval", fontSize = 14.sp, color = textPrimary)
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(6.dp))
                                        .background(Color(0xFF34C759).copy(alpha = 0.15f))
                                        .padding(horizontal = 8.dp, vertical = 2.dp)
                                ) {
                                    Text("92 • EXCELLENT", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF34C759))
                                }
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 2. SQUAD & PITCH INSET TABLE
        // =================================================================
        if (selectedSection == 0 || selectedSection == 2) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("02 // FIRST TEAM ROSTER & SQUAD MANAGEMENT", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(cardBg)
                    ) {
                        Column {
                            listOf(
                                Triple("9", "Jamie Tartt", Pair("ST", "88")),
                                Triple("14", "Dani Rojas", Pair("LW", "84")),
                                Triple("5", "Isaac McAdoo", Pair("CB", "86")),
                                Triple("8", "Roy Kent", Pair("CM", "83"))
                            ).forEachIndexed { index, (num, name, data) ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(horizontal = 16.dp, vertical = 12.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                                        Text(num, fontWeight = FontWeight.SemiBold, color = textSecondary, fontSize = 14.sp, modifier = Modifier.width(20.dp))
                                        Column {
                                            Text(name, fontWeight = FontWeight.SemiBold, fontSize = 15.sp, color = textPrimary)
                                            Text(data.first, fontSize = 12.sp, color = textSecondary)
                                        }
                                    }
                                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        Text(data.second, fontWeight = FontWeight.Bold, fontSize = 15.sp, color = appleBlue)
                                        Icon(Icons.AutoMirrored.Filled.ArrowForwardIos, contentDescription = null, tint = Color(0xFFC7C7CC), modifier = Modifier.size(12.dp))
                                    }
                                }
                                if (index < 3) {
                                    HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp, modifier = Modifier.padding(start = 50.dp))
                                }
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 3. MATCHES INSET GROUP
        // =================================================================
        if (selectedSection == 0 || selectedSection == 3) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("03 // FIXTURE CALENDAR & MATCH RESULTS", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(cardBg)
                    ) {
                        Column {
                            listOf(
                                Triple("Oct 14", "vs Arsenal (H)", Pair("3 - 1", Color(0xFF34C759))),
                                Triple("Oct 07", "@ Chelsea (A)", Pair("2 - 2", Color(0xFFFF9500))),
                                Triple("Sep 30", "vs Liverpool (H)", Pair("1 - 0", Color(0xFF34C759))),
                                Triple("Sep 23", "@ Man City (A)", Pair("0 - 2", Color(0xFFFF3B30)))
                            ).forEachIndexed { index, (date, fixture, result) ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(horizontal = 16.dp, vertical = 12.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                                        Text(date, fontSize = 12.sp, color = textSecondary, modifier = Modifier.width(48.dp))
                                        Text(fixture, fontWeight = FontWeight.Medium, fontSize = 14.sp, color = textPrimary)
                                    }
                                    Box(
                                        modifier = Modifier
                                            .clip(RoundedCornerShape(8.dp))
                                            .background(result.second.copy(alpha = 0.15f))
                                            .padding(horizontal = 10.dp, vertical = 3.dp)
                                    ) {
                                        Text(result.first, fontSize = 12.sp, fontWeight = FontWeight.Bold, color = result.second)
                                    }
                                }
                                if (index < 3) {
                                    HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp, modifier = Modifier.padding(start = 16.dp))
                                }
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 4. TRANSFERS INSET GROUP
        // =================================================================
        if (selectedSection == 0 || selectedSection == 4) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("04 // FINANCIAL ALLOCATION & TARGET NEGOTIATIONS", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(cardBg)
                    ) {
                        Column {
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("Transfer Liquidity", fontSize = 14.sp, color = textPrimary)
                                Text("€85,000,000", fontSize = 14.sp, color = textSecondary, fontWeight = FontWeight.Medium)
                            }
                            HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp, modifier = Modifier.padding(start = 16.dp))
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("Weekly Wage Budget", fontSize = 14.sp, color = textPrimary)
                                Text("€1,420,000", fontSize = 14.sp, color = textSecondary, fontWeight = FontWeight.Medium)
                            }
                            HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp, modifier = Modifier.padding(start = 16.dp))
                            Row(
                                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("Lucas Paquetá (Target)", fontSize = 14.sp, color = textPrimary)
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(6.dp))
                                        .background(appleBlue.copy(alpha = 0.12f))
                                        .padding(horizontal = 8.dp, vertical = 2.dp)
                                ) {
                                    Text("OFFER ACCEPTED", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = appleBlue)
                                }
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 5. YOUTH ACADEMY INSET GROUP
        // =================================================================
        if (selectedSection == 0 || selectedSection == 5) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("05 // YOUTH DEVELOPMENT & SCOUT MISSIONS", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(cardBg)
                    ) {
                        Column {
                            listOf(
                                Triple("Mateo Silva", "16 yo • CAM", "Pot. 88 - 94"),
                                Triple("Alvaro Gomez", "17 yo • RW", "Pot. 84 - 90"),
                                Triple("Lukas Meyer", "15 yo • CB", "Pot. 82 - 88")
                            ).forEachIndexed { index, (name, details, pot) ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(horizontal = 16.dp, vertical = 12.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Column {
                                        Text(name, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = textPrimary)
                                        Text(details, fontSize = 12.sp, color = textSecondary)
                                    }
                                    Box(
                                        modifier = Modifier
                                            .clip(RoundedCornerShape(6.dp))
                                            .background(Color(0xFF34C759).copy(alpha = 0.15f))
                                            .padding(horizontal = 8.dp, vertical = 3.dp)
                                    ) {
                                        Text(pot, fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF34C759))
                                    }
                                }
                                if (index < 2) {
                                    HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp, modifier = Modifier.padding(start = 16.dp))
                                }
                            }
                        }
                    }
                }
            }
        }

        // =================================================================
        // 6. CAREER HONOURS INSET GROUP
        // =================================================================
        if (selectedSection == 0 || selectedSection == 6) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("06 // CAREER HONOURS & MANAGER STATS", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(cardBg)
                    ) {
                        Column {
                            listOf(
                                Triple("Premier League Trophy", "Champions 2024/25", "Gold"),
                                Triple("UEFA Champions League", "Winners 2025/26", "Gold"),
                                Triple("FA Cup", "Winners 2024/25", "Silver")
                            ).forEachIndexed { index, (trophy, note, metal) ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(horizontal = 16.dp, vertical = 12.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                        Icon(
                                            Icons.Default.EmojiEvents,
                                            contentDescription = null,
                                            tint = if (metal == "Gold") Color(0xFFFF9500) else Color(0xFF8E8E93),
                                            modifier = Modifier.size(20.dp)
                                        )
                                        Column {
                                            Text(trophy, fontWeight = FontWeight.SemiBold, fontSize = 14.sp, color = textPrimary)
                                            Text(note, fontSize = 12.sp, color = textSecondary)
                                        }
                                    }
                                    Icon(Icons.AutoMirrored.Filled.ArrowForwardIos, contentDescription = null, tint = Color(0xFFC7C7CC), modifier = Modifier.size(12.dp))
                                }
                                if (index < 2) {
                                    HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp, modifier = Modifier.padding(start = 48.dp))
                                }
                            }
                        }
                    }
                }
            }
        }

        item { Spacer(Modifier.height(30.dp)) }
    }
}

// =========================================================================
// STYLE 3: APP ICON STUDIO (3 Interactive Concepts + Mask & Dock Preview)
// =========================================================================
@Composable
fun AppIconStudioMockup() {
    var selectedConcept by remember { mutableStateOf(0) }
    var selectedMask by remember { mutableStateOf(0) }

    val concepts = listOf(
        "Concept 1: Classic Matchday (Pitch & Match Ball)",
        "Concept 2: The Tactical Gaffer (Manager Tactics Board)",
        "Concept 3: Golden Silverware (Champions Trophy Crest)"
    )

    val masks = listOf(
        "Squircle (Adaptive)",
        "Circle (Pixel)",
        "Rounded Square (OneUI)",
        "Teardrop"
    )

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(Color(0xFF0F172A)).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        item {
            DesignExplainerHeader(
                name = "App Icon Design Studio",
                corePhilosophy = "Explore 3 distinct visual identities for FC Tracker, inspect adaptive icon masks, color palettes, and preview live on a simulated smartphone home screen dock.",
                keyElements = listOf("66dp Safe Zone Compliant", "Vector Geometric Precision", "Home Dock Simulation", "Subtle Gradient Depth")
            )
        }

        // Concept Selector Tabs
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("SELECT ICON CONCEPT", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF94A3B8), letterSpacing = 1.sp)
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    concepts.forEachIndexed { index, name ->
                        val isSelected = selectedConcept == index
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .clip(RoundedCornerShape(10.dp))
                                .background(if (isSelected) Color(0xFF2563EB) else Color(0xFF1E293B))
                                .clickable { selectedConcept = index }
                                .padding(vertical = 10.dp, horizontal = 6.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                "Design ${index + 1}",
                                color = if (isSelected) Color.White else Color(0xFF94A3B8),
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }
        }

        // Mask Shape Selector
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("ADAPTIVE MASK SHAPE", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF94A3B8), letterSpacing = 1.sp)
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    itemsIndexed(masks) { index, maskName ->
                        val isSelected = selectedMask == index
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(8.dp))
                                .background(if (isSelected) Color(0xFF38BDF8).copy(alpha = 0.2f) else Color(0xFF1E293B))
                                .border(1.dp, if (isSelected) Color(0xFF38BDF8) else Color.Transparent, RoundedCornerShape(8.dp))
                                .clickable { selectedMask = index }
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            Text(
                                maskName,
                                color = if (isSelected) Color(0xFF38BDF8) else Color(0xFF94A3B8),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.SemiBold
                            )
                        }
                    }
                }
            }
        }

        // Large Pedestal Showcase Preview
        item {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(24.dp))
                    .background(Color(0xFF1E293B))
                    .padding(24.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    Text(
                        concepts[selectedConcept],
                        fontWeight = FontWeight.Black,
                        fontSize = 17.sp,
                        color = Color.White
                    )

                    // Rendered App Icon with Mask
                    Box(
                        modifier = Modifier
                            .size(120.dp)
                            .shadow(16.dp, getMaskShape(selectedMask))
                            .clip(getMaskShape(selectedMask)),
                        contentAlignment = Alignment.Center
                    ) {
                        RenderIconCanvas(selectedConcept)
                    }

                    Text(
                        when (selectedConcept) {
                            0 -> "Vibrant Emerald Stadium Turf with Classic 3D Leather Match Ball, Penalty Arc & Victory Star"
                            1 -> "Tactical Pitch Whiteboard with Manager Formation Markers (X & O), Movement Arrows & Gold Whistle"
                            else -> "Regal European Night Crest with Golden Championship Trophy Cup, Laurels & Football Base"
                        },
                        fontSize = 11.sp,
                        color = Color(0xFF94A3B8),
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(horizontal = 16.dp)
                    )
                }
            }
        }

        // Smartphone Dock Simulation
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("SIMULATED SMARTPHONE HOME DOCK", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF94A3B8), letterSpacing = 1.sp)

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(130.dp)
                        .clip(RoundedCornerShape(24.dp))
                        .background(
                            Brush.verticalGradient(
                                listOf(Color(0xFF1E1B4B), Color(0xFF0F172A))
                            )
                        )
                        .padding(16.dp),
                    contentAlignment = Alignment.BottomCenter
                ) {
                    // Glass Dock Bar
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(84.dp)
                            .clip(RoundedCornerShape(22.dp))
                            .background(Color.White.copy(alpha = 0.12f))
                            .border(1.dp, Color.White.copy(alpha = 0.2f), RoundedCornerShape(22.dp))
                            .padding(horizontal = 16.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceAround,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            // Phone Icon
                            MockPhoneAppIcon("Phone", Icons.Default.Phone, Color(0xFF34C759))

                            // Messages Icon
                            MockPhoneAppIcon("Messages", Icons.Default.Chat, Color(0xFF007AFF))

                            // ACTIVE FC TRACKER ICON
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Box(
                                    modifier = Modifier
                                        .size(46.dp)
                                        .clip(getMaskShape(selectedMask)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    RenderIconCanvas(selectedConcept)
                                }
                                Spacer(Modifier.height(3.dp))
                                Text("FC Tracker", fontSize = 9.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            }

                            // Camera Icon
                            MockPhoneAppIcon("Camera", Icons.Default.PhotoCamera, Color(0xFF8E8E93))
                        }
                    }
                }
            }
        }

        // Design Specs & Color Palette Table
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("PALETTE & DESIGN SPECIFICATIONS", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF94A3B8), letterSpacing = 1.sp)

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(Color(0xFF1E293B))
                        .padding(16.dp)
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Safe Zone Compliance", fontSize = 13.sp, color = Color(0xFFCBD5E1))
                            Text("66dp / 108dp (100% Valid)", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = Color(0xFF34C759))
                        }
                        HorizontalDivider(color = Color(0xFF334155))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Active Color Swatches", fontSize = 13.sp, color = Color(0xFFCBD5E1))
                            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                val palette = when (selectedConcept) {
                                    0 -> listOf(Color(0xFF064E3B), Color(0xFFFFFFFF), Color(0xFF111827), Color(0xFFFBBF24))
                                    1 -> listOf(Color(0xFF0F172A), Color(0xFF38BDF8), Color(0xFFEF4444), Color(0xFFF59E0B))
                                    else -> listOf(Color(0xFF1E1B4B), Color(0xFFF59E0B), Color(0xFFFBBF24), Color(0xFF38BDF8))
                                }
                                palette.forEach { color ->
                                    Box(
                                        modifier = Modifier
                                            .size(18.dp)
                                            .clip(CircleShape)
                                            .background(color)
                                            .border(1.dp, Color.White.copy(alpha = 0.3f), CircleShape)
                                    )
                                }
                            }
                        }
                        HorizontalDivider(color = Color(0xFF334155))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Foreground Silhouette", fontSize = 13.sp, color = Color(0xFFCBD5E1))
                            Text(
                                when (selectedConcept) {
                                    0 -> "Matchday Soccer Ball & Pitch"
                                    1 -> "Manager Tactics Board & Arrows"
                                    else -> "Championship Cup Trophy"
                                },
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF38BDF8)
                            )
                        }
                    }
                }
            }
        }

        item { Spacer(Modifier.height(30.dp)) }
    }
}

// -------------------------------------------------------------------------
// Helper Components & Canvas Drawings
// -------------------------------------------------------------------------
fun getMaskShape(maskIndex: Int): androidx.compose.ui.graphics.Shape {
    return when (maskIndex) {
        1 -> CircleShape
        2 -> RoundedCornerShape(22.dp)
        3 -> RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp, bottomStart = 32.dp, bottomEnd = 8.dp)
        else -> RoundedCornerShape(28.dp) // Squircle
    }
}

@Composable
fun RenderIconCanvas(conceptIndex: Int) {
    Canvas(modifier = Modifier.fillMaxSize()) {
        val w = size.width
        val h = size.height

        when (conceptIndex) {
            0 -> {
                // CONCEPT 1: CLASSIC MATCHDAY (Emerald Stadium Turf & 3D Soccer Ball)
                // 1. Lush emerald stadium grass gradient
                drawRect(
                    brush = Brush.verticalGradient(
                        colors = listOf(Color(0xFF047857), Color(0xFF064E3B), Color(0xFF022C22)),
                        startY = 0f,
                        endY = h
                    )
                )

                // 2. Mown turf stadium stripe effect
                for (i in 0..4) {
                    if (i % 2 == 0) {
                        drawRect(
                            Color.White.copy(alpha = 0.04f),
                            topLeft = Offset(0f, h * (i * 0.2f)),
                            size = Size(w, h * 0.2f)
                        )
                    }
                }

                // 3. Pitch penalty box arc & markings in white
                drawArc(
                    color = Color.White.copy(alpha = 0.35f),
                    startAngle = 0f,
                    sweepAngle = 180f,
                    useCenter = false,
                    topLeft = Offset(w * 0.2f, h * 0.15f),
                    size = Size(w * 0.6f, h * 0.35f),
                    style = Stroke(width = 3.5f)
                )
                drawLine(
                    color = Color.White.copy(alpha = 0.35f),
                    start = Offset(w * 0.1f, h * 0.32f),
                    end = Offset(w * 0.9f, h * 0.32f),
                    strokeWidth = 3f
                )

                // 4. Drop shadow for soccer ball
                drawOval(
                    color = Color.Black.copy(alpha = 0.45f),
                    topLeft = Offset(w * 0.22f, h * 0.72f),
                    size = Size(w * 0.56f, h * 0.16f)
                )

                // 5. Soccer Ball Main Body (Classic 3D Sphere)
                val ballCenter = Offset(w * 0.5f, h * 0.52f)
                val ballRadius = w * 0.26f
                drawCircle(
                    brush = Brush.radialGradient(
                        colors = listOf(Color(0xFFFFFFFF), Color(0xFFE2E8F0), Color(0xFF94A3B8)),
                        center = Offset(ballCenter.x - ballRadius * 0.35f, ballCenter.y - ballRadius * 0.35f),
                        radius = ballRadius * 1.3f
                    ),
                    radius = ballRadius,
                    center = ballCenter
                )

                // 6. Central Black Pentagon
                val pentagonPath = Path().apply {
                    val pR = ballRadius * 0.38f
                    for (step in 0 until 5) {
                        val angle = (step * 72f - 90f) * (Math.PI / 180.0)
                        val px = ballCenter.x + (pR * Math.cos(angle)).toFloat()
                        val py = ballCenter.y + (pR * Math.sin(angle)).toFloat()
                        if (step == 0) moveTo(px, py) else lineTo(px, py)
                    }
                    close()
                }
                drawPath(pentagonPath, Color(0xFF111827))

                // 7. Outer Black Patches & Seams
                for (step in 0 until 5) {
                    val angle = (step * 72f - 90f) * (Math.PI / 180.0)
                    val pRInner = ballRadius * 0.38f
                    val pROuter = ballRadius * 0.78f
                    val innerX = ballCenter.x + (pRInner * Math.cos(angle)).toFloat()
                    val innerY = ballCenter.y + (pRInner * Math.sin(angle)).toFloat()
                    val outerX = ballCenter.x + (pROuter * Math.cos(angle)).toFloat()
                    val outerY = ballCenter.y + (pROuter * Math.sin(angle)).toFloat()
                    
                    // Seam line
                    drawLine(Color(0xFF334155), Offset(innerX, innerY), Offset(outerX, outerY), strokeWidth = 2.5f)

                    // Outer patch dot/arc
                    val patchRadius = ballRadius * 0.18f
                    val patchCenter = Offset(
                        ballCenter.x + (ballRadius * 0.88f * Math.cos(angle)).toFloat(),
                        ballCenter.y + (ballRadius * 0.88f * Math.sin(angle)).toFloat()
                    )
                    drawCircle(Color(0xFF1E293B), radius = patchRadius, center = patchCenter)
                }

                // Ball outer contour outline
                drawCircle(Color(0xFF0F172A), radius = ballRadius, center = ballCenter, style = Stroke(width = 3.5f))

                // 8. Golden Champions Star Overhead
                val starPath = Path().apply {
                    val cx = w * 0.5f
                    val cy = h * 0.16f
                    val rOut = w * 0.08f
                    val rIn = w * 0.035f
                    for (step in 0 until 10) {
                        val r = if (step % 2 == 0) rOut else rIn
                        val angle = (step * 36f - 90f) * (Math.PI / 180.0)
                        val sx = cx + (r * Math.cos(angle)).toFloat()
                        val sy = cy + (r * Math.sin(angle)).toFloat()
                        if (step == 0) moveTo(sx, sy) else lineTo(sx, sy)
                    }
                    close()
                }
                drawPath(starPath, Color(0xFFFBBF24))
            }

            1 -> {
                // CONCEPT 2: THE TACTICAL GAFFER (Manager Tactics Board & Whistle)
                // 1. Dark chalkboard/slate texture
                drawRect(
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFF0F172A), Color(0xFF1E293B), Color(0xFF0F172A)),
                        start = Offset(0f, 0f),
                        end = Offset(w, h)
                    )
                )

                // 2. Clipboard gold clip at the top
                drawRoundRect(
                    color = Color(0xFFF59E0B),
                    topLeft = Offset(w * 0.32f, h * 0.08f),
                    size = Size(w * 0.36f, h * 0.09f),
                    cornerRadius = CornerRadius(6f, 6f)
                )
                drawRoundRect(
                    color = Color(0xFFFBBF24),
                    topLeft = Offset(w * 0.38f, h * 0.11f),
                    size = Size(w * 0.24f, h * 0.035f),
                    cornerRadius = CornerRadius(4f, 4f)
                )

                // 3. Pitch boundary on the tactics board
                val pitchBox = Path().apply {
                    addRoundRect(
                        androidx.compose.ui.geometry.RoundRect(
                            w * 0.16f, h * 0.22f, w * 0.84f, h * 0.82f,
                            CornerRadius(10f, 10f)
                        )
                    )
                }
                drawPath(pitchBox, Color(0xFF064E3B).copy(alpha = 0.45f))
                drawPath(pitchBox, Color.White.copy(alpha = 0.4f), style = Stroke(width = 2.5f))

                // Half-way line & Center circle
                drawLine(Color.White.copy(alpha = 0.35f), Offset(w * 0.16f, h * 0.52f), Offset(w * 0.84f, h * 0.52f), strokeWidth = 2f)
                drawCircle(Color.White.copy(alpha = 0.35f), radius = w * 0.14f, center = Offset(w * 0.5f, h * 0.52f), style = Stroke(width = 2f))

                // Penalty Box at Top and Bottom
                drawRect(Color.White.copy(alpha = 0.3f), topLeft = Offset(w * 0.3f, h * 0.22f), size = Size(w * 0.4f, h * 0.14f), style = Stroke(width = 2f))
                drawRect(Color.White.copy(alpha = 0.3f), topLeft = Offset(w * 0.3f, h * 0.68f), size = Size(w * 0.4f, h * 0.14f), style = Stroke(width = 2f))

                // 4. Tactical Formation Player Markers (Blue = Midfield/Defense, Red = Strikers)
                // Defender markers (Cyan)
                drawCircle(Color(0xFF38BDF8), radius = w * 0.045f, center = Offset(w * 0.34f, h * 0.66f))
                drawCircle(Color(0xFF38BDF8), radius = w * 0.045f, center = Offset(w * 0.66f, h * 0.66f))

                // Midfield playmaker marker
                drawCircle(Color(0xFF06B6D4), radius = w * 0.052f, center = Offset(w * 0.5f, h * 0.50f))
                drawCircle(Color.White, radius = w * 0.02f, center = Offset(w * 0.5f, h * 0.50f))

                // Attacking Strikers (Crimson/Red)
                drawCircle(Color(0xFFEF4444), radius = w * 0.052f, center = Offset(w * 0.36f, h * 0.34f))
                drawCircle(Color(0xFFEF4444), radius = w * 0.052f, center = Offset(w * 0.64f, h * 0.34f))

                // 5. Attacking Curved Run Arrows in bright Neon Yellow
                val arrowPath = Path().apply {
                    moveTo(w * 0.5f, h * 0.46f)
                    quadraticTo(w * 0.58f, h * 0.40f, w * 0.62f, h * 0.37f)
                }
                drawPath(arrowPath, Color(0xFFFBBF24), style = Stroke(width = 3.5f))

                // Arrowhead
                val arrowHead = Path().apply {
                    moveTo(w * 0.65f, h * 0.35f)
                    lineTo(w * 0.60f, h * 0.34f)
                    lineTo(w * 0.62f, h * 0.40f)
                    close()
                }
                drawPath(arrowHead, Color(0xFFFBBF24))

                // 6. Gold Whistle Badge (Bottom-Right)
                drawCircle(Color(0xFFF59E0B), radius = w * 0.08f, center = Offset(w * 0.76f, h * 0.78f))
                drawRect(Color(0xFFD97706), topLeft = Offset(w * 0.72f, h * 0.74f), size = Size(w * 0.12f, h * 0.05f))
            }

            else -> {
                // CONCEPT 3: GOLDEN SILVERWARE (Champions Trophy Cup & Laurels)
                // 1. Royal Champions League purple-navy background
                drawRect(
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFF1E1B4B), Color(0xFF0F172A), Color(0xFF090D16)),
                        start = Offset(0f, 0f),
                        end = Offset(w, h)
                    )
                )

                // 2. Shimmering Golden Laurel Wreath
                drawArc(
                    color = Color(0xFFF59E0B),
                    startAngle = 100f,
                    sweepAngle = 150f,
                    useCenter = false,
                    topLeft = Offset(w * 0.12f, h * 0.22f),
                    size = Size(w * 0.36f, h * 0.55f),
                    style = Stroke(width = 5f)
                )
                drawArc(
                    color = Color(0xFFF59E0B),
                    startAngle = -70f,
                    sweepAngle = 150f,
                    useCenter = false,
                    topLeft = Offset(w * 0.52f, h * 0.22f),
                    size = Size(w * 0.36f, h * 0.55f),
                    style = Stroke(width = 5f)
                )

                // 3. Iconic Champions Cup Body (Big Ears Trophy)
                // Trophy Cup Chalice
                val cupPath = Path().apply {
                    moveTo(w * 0.32f, h * 0.26f)
                    lineTo(w * 0.68f, h * 0.26f)
                    cubicTo(w * 0.68f, h * 0.44f, w * 0.62f, h * 0.58f, w * 0.5f, h * 0.62f)
                    cubicTo(w * 0.38f, h * 0.58f, w * 0.32f, h * 0.44f, w * 0.32f, h * 0.26f)
                    close()
                }
                drawPath(
                    cupPath,
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFFFBBF24), Color(0xFFF59E0B), Color(0xFFD97706)),
                        start = Offset(w * 0.32f, h * 0.26f),
                        end = Offset(w * 0.68f, h * 0.62f)
                    )
                )

                // Trophy Handles ("Big Ears")
                val handleLeft = Path().apply {
                    moveTo(w * 0.32f, h * 0.28f)
                    cubicTo(w * 0.16f, h * 0.28f, w * 0.18f, h * 0.50f, w * 0.34f, h * 0.50f)
                }
                drawPath(handleLeft, Color(0xFFFBBF24), style = Stroke(width = 6f))

                val handleRight = Path().apply {
                    moveTo(w * 0.68f, h * 0.28f)
                    cubicTo(w * 0.84f, h * 0.28f, w * 0.82f, h * 0.50f, w * 0.66f, h * 0.50f)
                }
                drawPath(handleRight, Color(0xFFFBBF24), style = Stroke(width = 6f))

                // Trophy Stem & Base
                drawRect(
                    Color(0xFFF59E0B),
                    topLeft = Offset(w * 0.46f, h * 0.62f),
                    size = Size(w * 0.08f, h * 0.08f)
                )
                drawRoundRect(
                    Color(0xFFD97706),
                    topLeft = Offset(w * 0.34f, h * 0.70f),
                    size = Size(w * 0.32f, h * 0.06f),
                    cornerRadius = CornerRadius(4f, 4f)
                )

                // 4. Soccer Ball Inset on the Trophy Pedestal
                drawCircle(Color.White, radius = w * 0.045f, center = Offset(w * 0.5f, h * 0.73f))
                drawCircle(Color(0xFF111827), radius = w * 0.018f, center = Offset(w * 0.5f, h * 0.73f))

                // 5. Star on Cup
                val cupStar = Path().apply {
                    val cx = w * 0.5f
                    val cy = h * 0.38f
                    val rOut = w * 0.05f
                    val rIn = w * 0.022f
                    for (step in 0 until 10) {
                        val r = if (step % 2 == 0) rOut else rIn
                        val angle = (step * 36f - 90f) * (Math.PI / 180.0)
                        val sx = cx + (r * Math.cos(angle)).toFloat()
                        val sy = cy + (r * Math.sin(angle)).toFloat()
                        if (step == 0) moveTo(sx, sy) else lineTo(sx, sy)
                    }
                    close()
                }
                drawPath(cupStar, Color.White)
            }
        }
    }
}

@Composable
fun MockPhoneAppIcon(name: String, icon: androidx.compose.ui.graphics.vector.ImageVector, bgCol: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(
            modifier = Modifier
                .size(46.dp)
                .clip(RoundedCornerShape(12.dp))
                .background(bgCol),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(22.dp))
        }
        Spacer(Modifier.height(3.dp))
        Text(name, fontSize = 9.sp, color = Color.White.copy(alpha = 0.8f))
    }
}

@Composable
fun DesignExplainerHeader(name: String, corePhilosophy: String, keyElements: List<String>) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF1E293B))
            .padding(16.dp)
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(name, fontWeight = FontWeight.Black, fontSize = 16.sp, color = Color.White)
            Text(corePhilosophy, fontSize = 12.sp, color = Color(0xFFCBD5E1), lineHeight = 17.sp)
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                keyElements.take(2).forEach { elem ->
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(6.dp))
                            .background(Color(0xFF334155))
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text(elem, color = Color(0xFF93C5FD), fontSize = 10.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
    }
}

@Composable
fun TacticalNode(num: String, color: Color) {
    Box(
        modifier = Modifier
            .size(22.dp)
            .clip(CircleShape)
            .background(color),
        contentAlignment = Alignment.Center
    ) {
        Text(num, fontSize = 10.sp, fontWeight = FontWeight.Black, color = Color(0xFF0F172A))
    }
}
