import os

with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "w") as f:
    f.write("""package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
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
import androidx.compose.ui.window.Dialog
import com.example.AppState
import com.example.MainViewModel
import com.example.MatchResult
import com.example.PlayerPerformance
import com.example.ui.theme.DrawColor
import com.example.ui.theme.LossColor
import com.example.ui.theme.WinColor
import java.util.Calendar
import java.util.Date
import java.text.SimpleDateFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MatchesScreen(viewModel: MainViewModel, onMenuClick: () -> Unit) {
    val state by viewModel.state.collectAsState()
    var showMatchForm by remember { mutableStateOf(false) }
    var matchToEdit by remember { mutableStateOf<MatchResult?>(null) }
    
    // Calendar Logic
    val startYear = state.startYear
    val startCal = Calendar.getInstance().apply {
        set(Calendar.YEAR, startYear)
        set(Calendar.MONTH, Calendar.JULY)
        set(Calendar.DAY_OF_MONTH, 1)
    }
    val endCal = Calendar.getInstance().apply {
        set(Calendar.YEAR, startYear + 1)
        set(Calendar.MONTH, Calendar.JUNE)
        set(Calendar.DAY_OF_MONTH, 30)
    }
    
    // Determine active month based on the latest match, falling back to start month
    val df = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    val monthFmt = SimpleDateFormat("yyyy-MM", Locale.getDefault())
    
    var currentMonthCal by remember { 
        mutableStateOf(
            if (state.recentMatches.isNotEmpty()) {
                val latest = state.recentMatches.first().matchDate
                try {
                    val d = df.parse(latest)
                    Calendar.getInstance().apply { time = d; set(Calendar.DAY_OF_MONTH, 1) }
                } catch(e: Exception) {
                    startCal.clone() as Calendar
                }
            } else {
                startCal.clone() as Calendar
            }
        ) 
    }

    Box(modifier = Modifier.fillMaxSize()) {
        Column(modifier = Modifier.fillMaxSize()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(bottomStart = 24.dp, bottomEnd = 24.dp))
                    .background(MaterialTheme.colorScheme.surface)
                    .padding(20.dp)
                    .statusBarsPadding(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onMenuClick) {
                    Icon(Icons.Default.Menu, "Menu", tint = MaterialTheme.colorScheme.primary)
                }
                Text("Matches & Fixtures", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Box(modifier = Modifier.size(48.dp))
            }
            
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                item {
                    Text("Fixture Calendar", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                }
                
                item {
                    FixtureCalendar(
                        currentMonthCal = currentMonthCal,
                        onMonthChange = { newCal -> currentMonthCal = newCal },
                        startCal = startCal,
                        endCal = endCal,
                        matches = state.recentMatches
                    )
                }
                
                item { Spacer(Modifier.height(8.dp)) }
                item {
                    Text("Match History", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                }
                
                items(state.recentMatches) { match ->
                    MatchResultCard(
                        match = match, 
                        state = state,
                        onEdit = { matchToEdit = match; showMatchForm = true },
                        onDelete = { viewModel.deleteMatchResult(match.id) }
                    )
                }
                if (state.recentMatches.isEmpty()) {
                    item { Text("No matches played yet.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
                }
                item { Spacer(Modifier.height(80.dp)) }
            }
        }
        
        FloatingActionButton(
            onClick = { matchToEdit = null; showMatchForm = true },
            modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp),
            containerColor = MaterialTheme.colorScheme.primary
        ) {
            Icon(Icons.Default.Add, "Log Match", tint = MaterialTheme.colorScheme.onPrimary)
        }
        
        if (showMatchForm) {
            MatchFormModal(
                viewModel = viewModel, 
                state = state, 
                initialMatch = matchToEdit,
                onDismiss = { showMatchForm = false }, 
                onSave = { match -> 
                    if (matchToEdit != null) viewModel.updateMatchResult(match) 
                    else viewModel.addMatchResult(match)
                    showMatchForm = false 
                }
            )
        }
    }
}

@Composable
fun FixtureCalendar(currentMonthCal: Calendar, onMonthChange: (Calendar) -> Unit, startCal: Calendar, endCal: Calendar, matches: List<MatchResult>) {
    val monthFmt = SimpleDateFormat("MMMM yyyy", Locale.getDefault())
    val df = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    
    val matchesByDate = matches.groupBy { it.matchDate }
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(MaterialTheme.colorScheme.surface)
            .border(1.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(12.dp))
            .padding(16.dp)
    ) {
        Column {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = {
                    val prev = currentMonthCal.clone() as Calendar
                    prev.add(Calendar.MONTH, -1)
                    if (prev.timeInMillis >= startCal.timeInMillis || (prev.get(Calendar.YEAR) == startCal.get(Calendar.YEAR) && prev.get(Calendar.MONTH) == startCal.get(Calendar.MONTH))) {
                        onMonthChange(prev)
                    }
                }) {
                    Icon(Icons.Default.ArrowBack, contentDescription = "Prev Month", tint = Color.White)
                }
                Text(monthFmt.format(currentMonthCal.time), fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, fontSize = 16.sp)
                IconButton(onClick = {
                    val next = currentMonthCal.clone() as Calendar
                    next.add(Calendar.MONTH, 1)
                    if (next.timeInMillis <= endCal.timeInMillis || (next.get(Calendar.YEAR) == endCal.get(Calendar.YEAR) && next.get(Calendar.MONTH) == endCal.get(Calendar.MONTH))) {
                        onMonthChange(next)
                    }
                }) {
                    Icon(Icons.Default.ArrowForward, contentDescription = "Next Month", tint = Color.White)
                }
            }
            
            Spacer(Modifier.height(8.dp))
            
            // Days of week
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                listOf("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat").forEach {
                    Text(it, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f), textAlign = androidx.compose.ui.text.style.TextAlign.Center)
                }
            }
            
            Spacer(Modifier.height(8.dp))
            
            val cal = currentMonthCal.clone() as Calendar
            cal.set(Calendar.DAY_OF_MONTH, 1)
            val firstDayOfWeek = cal.get(Calendar.DAY_OF_WEEK) - 1 // 0 for Sun
            val daysInMonth = cal.getActualMaximum(Calendar.DAY_OF_MONTH)
            
            val totalCells = firstDayOfWeek + daysInMonth
            val rows = Math.ceil(totalCells / 7.0).toInt()
            
            Column {
                for (r in 0 until rows) {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                        for (c in 0 until 7) {
                            val cellIndex = r * 7 + c
                            val day = cellIndex - firstDayOfWeek + 1
                            if (day in 1..daysInMonth) {
                                val dateStr = String.format("%04d-%02d-%02d", cal.get(Calendar.YEAR), cal.get(Calendar.MONTH) + 1, day)
                                val dayMatches = matchesByDate[dateStr] ?: emptyList()
                                
                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .aspectRatio(1f)
                                        .padding(2.dp)
                                        .clip(CircleShape)
                                        .background(if (dayMatches.isNotEmpty()) MaterialTheme.colorScheme.primary else Color.Transparent),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = day.toString(), 
                                        color = if (dayMatches.isNotEmpty()) MaterialTheme.colorScheme.onPrimary else Color.White,
                                        fontSize = 12.sp
                                    )
                                }
                            } else {
                                Spacer(modifier = Modifier.weight(1f).aspectRatio(1f).padding(2.dp))
                            }
                        }
                    }
                }
            }
        }
    }
}
""")
