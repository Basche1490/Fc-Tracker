content = '''package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
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
        "3. Swiss Editorial Grid",
        "4. Floating Sheets & Sliders"
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
                    "UI Architecture Lab",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF111827)
                )
                Text(
                    "Compare 4 distinct minimalist layouts & elements",
                    fontSize = 12.sp,
                    color = Color(0xFF6B7280)
                )
            }
        }

        // Segmented Tab Row for the 4 Styles
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
                2 -> SwissEditorialStyleMockup()
                3 -> FloatingSlidersStyleMockup()
            }
        }
    }
}

// =========================================================================
// STYLE 1: BENTO MODULAR GRID
// Asymmetrical cards, embedded corner chips, radial badges, modular metrics
// =========================================================================
@Composable
fun BentoModularStyleMockup() {
    val bg = Color(0xFFF3F4F6)
    val cardBg = Color.White
    val accent = Color(0xFF2563EB)
    val textPrimary = Color(0xFF111827)
    val textSecondary = Color(0xFF6B7280)

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(bg).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(20.dp)
    ) {
        item {
            DesignExplainerHeader(
                name = "Bento Modular Grid",
                corePhilosophy = "Asymmetrical tiles, embedded status chips, modular stat grouping, and radial progress rings.",
                keyElements = listOf("Asymmetric Bento Boxes", "Embedded Corner Chips", "Circular Form Rings", "Modular Action Footers")
            )
        }

        // Section 1: Dashboard
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("DASHBOARD // BENTO TILES", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                // Large Hero Bento Tile
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
                            Text("Saturday, 15:00", fontSize = 12.sp, color = textSecondary)
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
                            modifier = Modifier.fillMaxWidth().height(48.dp)
                        ) {
                            Text("Enter Match Center", fontWeight = FontWeight.Bold)
                        }
                    }
                }

                // 2-Column Split Bento
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(20.dp))
                            .background(cardBg)
                            .padding(16.dp)
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text("RECENT FORM", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textSecondary)
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
                            Text("SQUAD MORALE", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                            Text("94%", fontSize = 26.sp, fontWeight = FontWeight.Black, color = Color(0xFF10B981))
                            Text("High dressing room trust", fontSize = 11.sp, color = textSecondary)
                        }
                    }
                }
            }
        }

        // Section 2: Squad List (Modular Cards)
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("SQUAD // MODULAR TILES", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                listOf(
                    Triple("Jamie Tartt", "ST", Pair("88", "Good")),
                    Triple("Dani Rojas", "LW", Pair("84", "Superb")),
                    Triple("Isaac McAdoo", "CB", Pair("86", "Normal"))
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
                                        Text("Form: ${data.second}", fontSize = 11.sp, color = textSecondary)
                                    }
                                }
                            }
                            Icon(Icons.AutoMirrored.Filled.ArrowForwardIos, contentDescription = null, tint = textSecondary, modifier = Modifier.size(14.dp))
                        }
                    }
                }
            }
        }

        // Section 3: Tactics (Tactile Stadium Bento)
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("TACTICS // SYSTEM TILE", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(24.dp))
                        .background(Color(0xFF0F172A))
                        .padding(20.dp)
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Column {
                                Text("TACTICAL STYLE", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = Color(0xFF94A3B8), letterSpacing = 1.sp)
                                Text("Custom 4-3-3 Attack", fontWeight = FontWeight.Black, color = Color.White, fontSize = 16.sp)
                            }
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(Color(0xFF1E293B))
                                    .padding(horizontal = 10.dp, vertical = 4.dp)
                            ) {
                                Text("TIKI-TAKA", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF38BDF8))
                            }
                        }

                        // Pitch Outline Box
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(150.dp)
                                .clip(RoundedCornerShape(16.dp))
                                .background(Color(0xFF1E293B))
                                .border(1.dp, Color(0xFF334155), RoundedCornerShape(16.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(
                                modifier = Modifier.fillMaxSize().padding(16.dp),
                                verticalArrangement = Arrangement.SpaceBetween,
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                                    repeat(3) { TacticalNode("9", Color(0xFF38BDF8)) }
                                }
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                                    repeat(3) { TacticalNode("8", Color(0xFF818CF8)) }
                                }
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                                    repeat(4) { TacticalNode("4", Color(0xFF94A3B8)) }
                                }
                            }
                        }
                    }
                }
            }
        }

        // Section 4: Finances (Metric Bento Split)
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("FINANCES // METRIC TILES", fontSize = 11.sp, fontWeight = FontWeight.Black, color = textSecondary, letterSpacing = 1.5.sp)

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
            }
        }

        item { Spacer(Modifier.height(30.dp)) }
    }
}

// =========================================================================
// STYLE 2: APPLE INSET & SEGMENTED (iOS Native Sports Feel)
// Edge-to-edge grouped rows, hairline dividers, segmented pills, micro-chips
// =========================================================================
@Composable
fun AppleInsetSegmentedStyleMockup() {
    val bg = Color(0xFFF2F2F7) // iOS system background
    val cardBg = Color.White
    val textPrimary = Color(0xFF000000)
    val textSecondary = Color(0xFF8E8E93)
    val appleBlue = Color(0xFF007AFF)

    var segmentedTab by remember { mutableStateOf(0) }

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(bg).padding(horizontal = 16.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(22.dp)
    ) {
        item {
            DesignExplainerHeader(
                name = "Apple Inset & Segmented",
                corePhilosophy = "Cardless grouped rows, hairline dividers, inline segmented controls, and generous vertical whitespace.",
                keyElements = listOf("Hairline Separators (0.5dp)", "Inset Grouped Lists", "Segmented Header Pills", "Micro Badge Chips")
            )
        }

        // Section 1: Dashboard Inset Group
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("UPCOMING FIXTURE", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

                // Inset Group
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(cardBg)
                ) {
                    Column {
                        // Segmented Control inside
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
                                            .background(if (segmentedTab == i) Color.White else Color.Transparent)
                                            .clickable { segmentedTab = i }
                                            .padding(vertical = 6.dp),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text(
                                            title,
                                            fontSize = 12.sp,
                                            fontWeight = if (segmentedTab == i) FontWeight.Bold else FontWeight.Normal,
                                            color = if (segmentedTab == i) textPrimary else textSecondary
                                        )
                                    }
                                }
                            }
                        }

                        HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp)

                        // Clean Match Row
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
            }
        }

        // Section 2: Squad Inset Table
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("FIRST TEAM ROSTER", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

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

        // Section 3: Clean Key-Value Settings Rows
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("CLUB STATUS", fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = textSecondary, modifier = Modifier.padding(start = 12.dp))

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
                            Text("Available Transfer Funds", fontSize = 15.sp, color = textPrimary)
                            Text("€85,000,000", fontSize = 15.sp, color = textSecondary)
                        }
                        HorizontalDivider(color = Color(0xFFE5E5EA), thickness = 0.5.dp, modifier = Modifier.padding(start = 16.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text("Board Objective Rating", fontSize = 15.sp, color = textPrimary)
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(6.dp))
                                    .background(Color(0xFF34C759).copy(alpha = 0.15f))
                                    .padding(horizontal = 8.dp, vertical = 2.dp)
                            ) {
                                Text("EXCELLENT", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = Color(0xFF34C759))
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
// STYLE 3: SWISS EDITORIAL / TYPOGRAPHIC GRID
// Giant display numerals, hairline rulers, strict 0dp corners, newspaper columns
// =========================================================================
@Composable
fun SwissEditorialStyleMockup() {
    val bg = Color(0xFFFFFFFF)
    val borderCol = Color(0xFF111827)
    val textPrimary = Color(0xFF111827)
    val textSecondary = Color(0xFF6B7280)

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(bg).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        item {
            DesignExplainerHeader(
                name = "Swiss Editorial Grid",
                corePhilosophy = "Massive tabular numbers, strict 0dp rectangular geometry, cross-grid rulers, and brutalist typographic hierarchy.",
                keyElements = listOf("Stark Tabular Numerals", "0dp Sharp Corners", "1px Hairline Grid Rulers", "Editorial Column Alignment")
            )
        }

        // Section 1: Editorial Headline Match Card
        item {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .border(2.dp, borderCol)
            ) {
                // Header bar
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(borderCol)
                        .padding(horizontal = 12.dp, vertical = 6.dp),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("VOL. 24 // MATCHDAY 18", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Black, letterSpacing = 2.sp)
                    Text("PREMIER DIVISION", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }

                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("RICHMOND FC", fontSize = 28.sp, fontWeight = FontWeight.Black, color = textPrimary, letterSpacing = (-0.5).sp)
                    Text("VERSUS", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textSecondary, letterSpacing = 2.sp)
                    Text("ARSENAL FC", fontSize = 28.sp, fontWeight = FontWeight.Black, color = textPrimary, letterSpacing = (-0.5).sp)

                    HorizontalDivider(color = borderCol, thickness = 1.dp)

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("15:00 BST // SELHURST PARK", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                        Box(
                            modifier = Modifier
                                .border(1.dp, borderCol)
                                .padding(horizontal = 12.dp, vertical = 4.dp)
                        ) {
                            Text("SIMULATE", fontSize = 11.sp, fontWeight = FontWeight.Black, color = borderCol)
                        }
                    }
                }
            }
        }

        // Section 2: Tabular Column Roster
        item {
            Column(modifier = Modifier.fillMaxWidth()) {
                Text("02 // SQUAD COMPOSITION", fontSize = 12.sp, fontWeight = FontWeight.Black, color = textPrimary, letterSpacing = 1.sp)
                Spacer(Modifier.height(8.dp))

                Column(modifier = Modifier.fillMaxWidth().border(1.dp, borderCol)) {
                    // Column Headers
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0xFFF3F4F6))
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("POS", fontSize = 11.sp, fontWeight = FontWeight.Black, modifier = Modifier.width(36.dp))
                        Text("PLAYER NAME", fontSize = 11.sp, fontWeight = FontWeight.Black, modifier = Modifier.weight(1f))
                        Text("AGE", fontSize = 11.sp, fontWeight = FontWeight.Black, modifier = Modifier.width(36.dp), textAlign = TextAlign.End)
                        Text("OVR", fontSize = 11.sp, fontWeight = FontWeight.Black, modifier = Modifier.width(44.dp), textAlign = TextAlign.End)
                    }
                    HorizontalDivider(color = borderCol, thickness = 1.dp)

                    listOf(
                        listOf("ST", "J. Tartt", "26", "88"),
                        listOf("LW", "D. Rojas", "24", "84"),
                        listOf("CM", "R. Kent", "34", "83"),
                        listOf("CB", "I. McAdoo", "27", "86")
                    ).forEachIndexed { i, row ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 12.dp, vertical = 10.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(row[0], fontSize = 12.sp, fontWeight = FontWeight.Black, color = borderCol, modifier = Modifier.width(36.dp))
                            Text(row[1], fontSize = 13.sp, fontWeight = FontWeight.Bold, color = textPrimary, modifier = Modifier.weight(1f))
                            Text(row[2], fontSize = 12.sp, color = textSecondary, modifier = Modifier.width(36.dp), textAlign = TextAlign.End)
                            Text(row[3], fontSize = 14.sp, fontWeight = FontWeight.Black, color = borderCol, modifier = Modifier.width(44.dp), textAlign = TextAlign.End)
                        }
                        if (i < 3) HorizontalDivider(color = Color(0xFFE5E7EB), thickness = 1.dp)
                    }
                }
            }
        }

        // Section 3: Large Display Metrics
        item {
            Column(modifier = Modifier.fillMaxWidth()) {
                Text("03 // FISCAL POSITION", fontSize = 12.sp, fontWeight = FontWeight.Black, color = textPrimary, letterSpacing = 1.sp)
                Spacer(Modifier.height(8.dp))

                Row(modifier = Modifier.fillMaxWidth().border(1.dp, borderCol)) {
                    Column(modifier = Modifier.weight(1f).padding(16.dp)) {
                        Text("TRANSFER LIQUIDITY", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                        Spacer(Modifier.height(4.dp))
                        Text("€85M", fontSize = 32.sp, fontWeight = FontWeight.Black, color = textPrimary)
                    }
                    Box(modifier = Modifier.width(1.dp).fillMaxHeight().background(borderCol))
                    Column(modifier = Modifier.weight(1f).padding(16.dp)) {
                        Text("LEAGUE POSITION", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = textSecondary)
                        Spacer(Modifier.height(4.dp))
                        Text("1ST", fontSize = 32.sp, fontWeight = FontWeight.Black, color = textPrimary)
                    }
                }
            }
        }

        item { Spacer(Modifier.height(30.dp)) }
    }
}

// =========================================================================
// STYLE 4: FLOATING SHEETS & SLIDERS
// Pill containers, interactive micro-sliders, horizontal player passport cards
// =========================================================================
@Composable
fun FloatingSlidersStyleMockup() {
    val bg = Color(0xFFFAFAFA)
    val cardBg = Color.White
    val primary = Color(0xFF4F46E5) // Indigo
    val textPrimary = Color(0xFF1E1B4B)
    val textSecondary = Color(0xFF6B7280)

    var tempoSlider by remember { mutableStateOf(0.7f) }
    var widthSlider by remember { mutableStateOf(0.5f) }

    LazyColumn(
        modifier = Modifier.fillMaxSize().background(bg).padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(22.dp)
    ) {
        item {
            DesignExplainerHeader(
                name = "Floating Sheets & Sliders",
                corePhilosophy = "Tactile pill sliders, floating passport cards, rounded micro-surfaces, and interactive visual tracks.",
                keyElements = listOf("Tactile Micro-Sliders", "Horizontal Player Passports", "Pill Floating Dock", "Attribute Progress Tracks")
            )
        }

        // Section 1: Floating Hero Card
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("MATCH CENTER // FLOATING CARD", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textSecondary, letterSpacing = 1.sp)

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(28.dp))
                        .background(cardBg)
                        .border(1.dp, Color(0xFFE0E7FF), RoundedCornerShape(28.dp))
                        .padding(20.dp)
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("NEXT FIXTURE", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = primary)
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(12.dp))
                                    .background(Color(0xFFEEF2FF))
                                    .padding(horizontal = 10.dp, vertical = 4.dp)
                            ) {
                                Text("In 3 Days", fontSize = 11.sp, fontWeight = FontWeight.SemiBold, color = primary)
                            }
                        }

                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            Text("Richmond FC", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = textPrimary)
                            Text("vs", color = textSecondary, fontWeight = FontWeight.Medium)
                            Text("Arsenal FC", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = textPrimary)
                        }

                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(16.dp))
                                .background(primary)
                                .clickable { }
                                .padding(vertical = 12.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("Simulate Matchday", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        }
                    }
                }
            }
        }

        // Section 2: Tactical Sliders
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("TACTICAL SLIDERS // TACTILE INPUT", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textSecondary, letterSpacing = 1.sp)

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(24.dp))
                        .background(cardBg)
                        .border(1.dp, Color(0xFFF3F4F6), RoundedCornerShape(24.dp))
                        .padding(20.dp)
                ) {
                    Column(verticalArrangement = Arrangement.spacedBy(18.dp)) {
                        Column {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Team Tempo", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = textPrimary)
                                Text(if (tempoSlider > 0.6f) "High" else "Balanced", fontSize = 12.sp, color = primary, fontWeight = FontWeight.Bold)
                            }
                            Slider(
                                value = tempoSlider,
                                onValueChange = { tempoSlider = it },
                                colors = SliderDefaults.colors(thumbColor = primary, activeTrackColor = primary)
                            )
                        }

                        Column {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Offensive Width", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = textPrimary)
                                Text(if (widthSlider > 0.6f) "Wide" else "Narrow", fontSize = 12.sp, color = primary, fontWeight = FontWeight.Bold)
                            }
                            Slider(
                                value = widthSlider,
                                onValueChange = { widthSlider = it },
                                colors = SliderDefaults.colors(thumbColor = primary, activeTrackColor = primary)
                            )
                        }
                    }
                }
            }
        }

        // Section 3: Player Passport Slips
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Text("PLAYER PASSPORTS // HORIZONTAL SLIPS", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = textSecondary, letterSpacing = 1.sp)

                listOf(
                    Pair("Jamie Tartt", "ST // OVR 88"),
                    Pair("Dani Rojas", "LW // OVR 84")
                ).forEach { (name, sub) ->
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(20.dp))
                            .background(cardBg)
                            .border(1.dp, Color(0xFFF3F4F6), RoundedCornerShape(20.dp))
                            .padding(16.dp)
                    ) {
                        Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
                            Column {
                                Text(name, fontSize = 15.sp, fontWeight = FontWeight.Bold, color = textPrimary)
                                Text(sub, fontSize = 12.sp, color = textSecondary)
                                Spacer(Modifier.height(6.dp))
                                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                    Box(modifier = Modifier.size(40.dp, 4.dp).clip(CircleShape).background(Color(0xFF10B981)))
                                    Box(modifier = Modifier.size(40.dp, 4.dp).clip(CircleShape).background(Color(0xFF10B981)))
                                    Box(modifier = Modifier.size(20.dp, 4.dp).clip(CircleShape).background(Color(0xFFE5E7EB)))
                                }
                            }
                            Box(
                                modifier = Modifier
                                    .size(36.dp)
                                    .clip(CircleShape)
                                    .background(Color(0xFFF3F4F6)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Edit, null, tint = textSecondary, modifier = Modifier.size(16.dp))
                            }
                        }
                    }
                }
            }
        }

        item { Spacer(Modifier.height(30.dp)) }
    }
}

// -------------------------------------------------------------------------
// Helper Components
// -------------------------------------------------------------------------
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
'''

with open("app/src/main/java/com/example/ui/screens/MockDesignGalleryScreen.kt", "w") as f:
    f.write(content)
print("Updated MockDesignGalleryScreen.kt successfully!")
