cat << 'INNER_EOF' > app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt.patch
package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.MainViewModel
import com.example.Player
import com.example.ui.theme.WinColor

@Composable
fun CareerSummaryScreen(viewModel: MainViewModel, onMenuClick: () -> Unit) {
    val state by viewModel.state.collectAsState()

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            @OptIn(ExperimentalMaterial3Api::class)
            TopAppBar(
                title = { Text("Career Summary", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground) },
                navigationIcon = {
                    IconButton(onClick = onMenuClick) {
                        Icon(Icons.Default.Menu, contentDescription = "Menu", tint = MaterialTheme.colorScheme.primary)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.onBackground
                )
            )
        }
    ) { padding ->
        var selectedPlayer by remember { mutableStateOf<Player?>(null) }

        Box(modifier = Modifier.padding(padding).fillMaxSize()) {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                item {
                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Text("Overall Manager Statistics", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                        Spacer(modifier = Modifier.height(12.dp))
                        
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            OutlinedTextField(value = "0", onValueChange = {}, label = { Text("League Titles") }, modifier = Modifier.weight(1f), readOnly = true)
                            OutlinedTextField(value = "0", onValueChange = {}, label = { Text("Domestic Cups") }, modifier = Modifier.weight(1f), readOnly = true)
                            OutlinedTextField(value = "0", onValueChange = {}, label = { Text("Continental") }, modifier = Modifier.weight(1f), readOnly = true)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            OutlinedTextField(value = "25", onValueChange = {}, label = { Text("Wins") }, modifier = Modifier.weight(1f), readOnly = true)
                            OutlinedTextField(value = "6", onValueChange = {}, label = { Text("Draws") }, modifier = Modifier.weight(1f), readOnly = true)
                            OutlinedTextField(value = "4", onValueChange = {}, label = { Text("Losses") }, modifier = Modifier.weight(1f), readOnly = true)
                        }
                    }
                }
                
                item {
                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Text("Hall of Fame (Best Players)", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Name", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(2f))
                            Text("Apps", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                            Text("Gls", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                            Text("Ast", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        
                        val topPlayers = state.players.sortedByDescending { it.averageRating }.take(5)
                        topPlayers.forEach { player ->
                            Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(2f)) {
                                    Box(modifier = Modifier.size(24.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant), contentAlignment = Alignment.Center) {
                                        Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(16.dp))
                                    }
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("${player.firstName.first()}. ${player.lastName}", color = Color.White, fontSize = 12.sp)
                                }
                                Text("${player.matchesPlayed}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                                Text("${player.goals}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                                Text("${player.assists}", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                            }
                            HorizontalDivider(color = MaterialTheme.colorScheme.surfaceVariant)
                        }
                    }
                }
                item {
                    DarkCard(modifier = Modifier.fillMaxWidth()) {
                        Text("Club Milestones & Record Holders", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                        Spacer(modifier = Modifier.height(12.dp))
                        
                        RecordCard("Most Appearances", "J. Tartt", "15")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("All-Time Top Scorer", "J. Tartt", "12")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("All-Time Top Assists", "S. Obisanya", "6")
                        Spacer(Modifier.height(8.dp))
                        RecordCard("Highest Rated Transfer", "L. Messi", "€50M")
                    }
                }
                item {
                    Button(onClick = { /* Export Logic */ }, modifier = Modifier.fillMaxWidth()) {
                        Text("Export Career Data (CSV)")
                    }
                    Spacer(Modifier.height(80.dp))
                }
            }
        }
    }
}

@Composable
fun RecordCard(title: String, holder: String, value: String) {
    Box(modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(8.dp)).background(MaterialTheme.colorScheme.surfaceVariant).padding(12.dp)) {
        Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Column {
                Text(title, fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(holder, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
            }
            Text(value, fontSize = 18.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
fun DarkCard(modifier: Modifier = Modifier, content: @Composable ColumnScope.() -> Unit) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface)
            .border(1.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column(content = content)
    }
}
INNER_EOF
mv app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt.patch app/src/main/java/com/example/ui/screens/CareerSummaryScreen.kt
