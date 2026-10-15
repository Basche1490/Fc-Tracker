cat << 'INNER_EOF' > app/src/main/java/com/example/ui/screens/SeasonSummaryScreen.kt
package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.MainViewModel
import com.example.AppState
import com.example.ClubObjective

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SeasonSummaryScreen(viewModel: MainViewModel, onMenuClick: () -> Unit) {
    val state by viewModel.state.collectAsState()
    var selectedTabIndex by remember { mutableStateOf(0) }
    val tabs = listOf("Overview", "Squad & Awards", "Board Review")
    
    var showAwardsModal by remember { mutableStateOf(false) }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            TopAppBar(
                title = { Text("Season Summary", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground) },
                navigationIcon = {
                    IconButton(onClick = onMenuClick) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu", tint = MaterialTheme.colorScheme.primary)
                    }
                },
                actions = {
                    Button(
                        onClick = { /* End Season Logic */ },
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                        modifier = Modifier.padding(end = 8.dp)
                    ) {
                        Text("End Season", color = MaterialTheme.colorScheme.onErrorContainer)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.onBackground
                )
            )
        }
    ) { padding ->
        Column(modifier = Modifier.padding(padding).fillMaxSize()) {
            TabRow(
                selectedTabIndex = selectedTabIndex,
                containerColor = MaterialTheme.colorScheme.surface,
                contentColor = MaterialTheme.colorScheme.primary,
                indicator = { tabPositions ->
                    if (selectedTabIndex < tabPositions.size) {
                        TabRowDefaults.SecondaryIndicator(
                            Modifier.tabIndicatorOffset(tabPositions[selectedTabIndex]),
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            ) {
                tabs.forEachIndexed { index, title ->
                    Tab(
                        selected = selectedTabIndex == index,
                        onClick = { selectedTabIndex = index },
                        text = { Text(title, fontWeight = FontWeight.Bold) }
                    )
                }
            }
            
            when (selectedTabIndex) {
                0 -> OverviewTab(state, viewModel)
                1 -> SquadStatsAwardsTab(state) { showAwardsModal = true }
                2 -> FinanceBoardTab(state)
            }
        }
    }
    
    if (showAwardsModal) {
        AwardsModal(onDismiss = { showAwardsModal = false })
    }
}

@Composable
fun OverviewTab(state: AppState, viewModel: MainViewModel) {
    var showAddObjective by remember { mutableStateOf(false) }

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("Season Analytics Visualized", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                // Simple Canvas Chart Placeholder
                androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxWidth().height(150.dp)) {
                    val path = androidx.compose.ui.graphics.Path()
                    path.moveTo(0f, size.height)
                    path.lineTo(size.width * 0.2f, size.height * 0.8f)
                    path.lineTo(size.width * 0.4f, size.height * 0.9f)
                    path.lineTo(size.width * 0.6f, size.height * 0.5f)
                    path.lineTo(size.width * 0.8f, size.height * 0.4f)
                    path.lineTo(size.width, size.height * 0.1f)
                    
                    drawPath(
                        path = path,
                        color = Color(0xFF4CAF50),
                        style = androidx.compose.ui.graphics.drawscope.Stroke(width = 8f)
                    )
                }
                Text("Manager Rating Trend", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp, modifier = Modifier.align(Alignment.CenterHorizontally))
            }
        }
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Text("Club Objectives Master Panel", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                    IconButton(onClick = { showAddObjective = true }) {
                        Icon(Icons.Default.Add, contentDescription = "Add Objective", tint = MaterialTheme.colorScheme.primary)
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text("Manage and track long term objectives here.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 12.sp)
                
                state.objectives.forEach { obj ->
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { 
                            viewModel.updateObjective(obj.copy(isCompleted = !obj.isCompleted)) 
                        }
                    ) {
                        Checkbox(checked = obj.isCompleted, onCheckedChange = { viewModel.updateObjective(obj.copy(isCompleted = it)) })
                        Column(modifier = Modifier.weight(1f)) {
                            Text(obj.title, color = Color.White)
                            Text("Priority: \${obj.priority}", fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        IconButton(onClick = { viewModel.deleteObjective(obj.id) }) {
                            Icon(Icons.Default.Delete, contentDescription = "Delete", tint = Color.Red.copy(alpha=0.7f))
                        }
                    }
                }
            }
        }
        item { Spacer(Modifier.height(80.dp)) }
    }

    if (showAddObjective) {
        var objTitle by remember { mutableStateOf("") }
        var objPriority by remember { mutableStateOf("Medium") }
        Dialog(onDismissRequest = { showAddObjective = false }) {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("Add Objective", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(value = objTitle, onValueChange = { objTitle = it }, label = { Text("Title") }, modifier = Modifier.fillMaxWidth())
                @OptIn(ExperimentalMaterial3Api::class)
                var expanded by remember { mutableStateOf(false) }
                @OptIn(ExperimentalMaterial3Api::class)
                ExposedDropdownMenuBox(
                    expanded = expanded,
                    onExpandedChange = { expanded = !expanded },
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)
                ) {
                    OutlinedTextField(
                        value = objPriority,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Priority") },
                        modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(),
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) }
                    )
                    ExposedDropdownMenu(
                        expanded = expanded,
                        onDismissRequest = { expanded = false }
                    ) {
                        listOf("Low", "Medium", "High").forEach { selectionOption ->
                            DropdownMenuItem(
                                text = { Text(selectionOption) },
                                onClick = {
                                    objPriority = selectionOption
                                    expanded = false
                                }
                            )
                        }
                    }
                }
                Spacer(Modifier.height(16.dp))
                Button(onClick = {
                    viewModel.addObjective(ClubObjective(title = objTitle, priority = objPriority))
                    showAddObjective = false
                }, modifier = Modifier.align(Alignment.End)) {
                    Text("Add")
                }
            }
        }
    }
}

@Composable
fun SquadStatsAwardsTab(state: AppState, onAssignAwards: () -> Unit) {
    var selectedPlayer by remember { mutableStateOf<com.example.Player?>(null) }
    
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Button(onClick = onAssignAwards, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)) {
                Text("Assign Awards & Honors")
            }
        }
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("Season Player Statistics", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                
                Row(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Player", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(2f))
                    Text("Apps", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                    Text("Gls", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                    Text("Asts", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, modifier = Modifier.weight(1f))
                }
                
                state.players.forEach { player ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { selectedPlayer = player }
                            .padding(vertical = 8.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("\${player.firstName} \${player.lastName}", color = Color.White, modifier = Modifier.weight(2f))
                        Text("\${player.matchesPlayed}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text("\${player.goals}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        Text("\${player.assists}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                    }
                    HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant)
                }
            }
        }
    }
    
    if (selectedPlayer != null) {
        Dialog(onDismissRequest = { selectedPlayer = null }) {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("\${selectedPlayer?.firstName} \${selectedPlayer?.lastName} Season Breakdown", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(Modifier.height(16.dp))
                Button(onClick = { selectedPlayer = null }, modifier = Modifier.align(Alignment.End)) {
                    Text("Close")
                }
            }
        }
    }
}

@Composable
fun FinanceBoardTab(state: AppState) {
    // Calculate rating
    var score = 0
    var totalPossible = 0
    state.objectives.forEach {
        val weight = when (it.priority) {
            "High" -> 3
            "Medium" -> 2
            else -> 1
        }
        totalPossible += weight
        if (it.isCompleted) score += weight
    }
    
    val percentage = if (totalPossible > 0) score.toFloat() / totalPossible else 1f
    val rating = when {
        percentage >= 0.9f -> "A+"
        percentage >= 0.8f -> "A"
        percentage >= 0.7f -> "B+"
        percentage >= 0.6f -> "B"
        percentage >= 0.4f -> "C"
        percentage >= 0.2f -> "D"
        else -> "F"
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("Board Review", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                Text("Manager Rating: \$rating", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                Text("Trust Level: \${if (percentage > 0.6) "High" else "Low"}", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        item {
            DarkCard(modifier = Modifier.fillMaxWidth()) {
                Text("Financial Summary", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(modifier = Modifier.height(8.dp))
                Text("Total Income: €120M", color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("Total Expenses: €95M", color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("Net Profit: €25M", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun AwardsModal(onDismiss: () -> Unit) {
    Dialog(onDismissRequest = onDismiss) {
        DarkCard(modifier = Modifier.fillMaxWidth()) {
            Text("Awards Placeholder", color = Color.White)
        }
    }
}
INNER_EOF
