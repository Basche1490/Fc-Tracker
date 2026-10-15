import re

def rewrite():
    content = """package com.example.ui.screens

import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.ui.layout.boundsInRoot
import androidx.compose.ui.layout.boundsInWindow
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInRoot
import androidx.compose.ui.layout.positionInWindow
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import com.example.Player

data class FormationPos(val x: Float, val y: Float)

val formationsMap = mapOf(
    "4-3-3" to listOf(
        FormationPos(0.5f, 0.9f), // GK
        FormationPos(0.15f, 0.7f), // LB
        FormationPos(0.35f, 0.75f), // CB
        FormationPos(0.65f, 0.75f), // CB
        FormationPos(0.85f, 0.7f), // RB
        FormationPos(0.25f, 0.45f), // CM
        FormationPos(0.5f, 0.5f), // CM
        FormationPos(0.75f, 0.45f), // CM
        FormationPos(0.2f, 0.2f), // LW
        FormationPos(0.5f, 0.15f), // ST
        FormationPos(0.8f, 0.2f) // RW
    ),
    "4-2-3-1" to listOf(
        FormationPos(0.5f, 0.9f), // GK
        FormationPos(0.15f, 0.7f), // LB
        FormationPos(0.35f, 0.75f), // CB
        FormationPos(0.65f, 0.75f), // CB
        FormationPos(0.85f, 0.7f), // RB
        FormationPos(0.35f, 0.55f), // CDM
        FormationPos(0.65f, 0.55f), // CDM
        FormationPos(0.2f, 0.35f), // LAM
        FormationPos(0.5f, 0.3f), // CAM
        FormationPos(0.8f, 0.35f), // RAM
        FormationPos(0.5f, 0.15f) // ST
    ),
    "4-4-2" to listOf(
        FormationPos(0.5f, 0.9f), // GK
        FormationPos(0.15f, 0.7f), // LB
        FormationPos(0.35f, 0.75f), // CB
        FormationPos(0.65f, 0.75f), // CB
        FormationPos(0.85f, 0.7f), // RB
        FormationPos(0.15f, 0.45f), // LM
        FormationPos(0.35f, 0.45f), // CM
        FormationPos(0.65f, 0.45f), // CM
        FormationPos(0.85f, 0.45f), // RM
        FormationPos(0.35f, 0.15f), // ST
        FormationPos(0.65f, 0.15f) // ST
    ),
    "3-5-2" to listOf(
        FormationPos(0.5f, 0.9f), // GK
        FormationPos(0.25f, 0.75f), // CB
        FormationPos(0.5f, 0.75f), // CB
        FormationPos(0.75f, 0.75f), // CB
        FormationPos(0.15f, 0.45f), // LWB
        FormationPos(0.35f, 0.55f), // CDM
        FormationPos(0.5f, 0.4f), // CAM
        FormationPos(0.65f, 0.55f), // CDM
        FormationPos(0.85f, 0.45f), // RWB
        FormationPos(0.35f, 0.15f), // ST
        FormationPos(0.65f, 0.15f) // ST
    ),
    "5-3-2" to listOf(
        FormationPos(0.5f, 0.9f), // GK
        FormationPos(0.1f, 0.65f), // LWB
        FormationPos(0.3f, 0.75f), // CB
        FormationPos(0.5f, 0.75f), // CB
        FormationPos(0.7f, 0.75f), // CB
        FormationPos(0.9f, 0.65f), // RWB
        FormationPos(0.25f, 0.45f), // CM
        FormationPos(0.5f, 0.45f), // CM
        FormationPos(0.75f, 0.45f), // CM
        FormationPos(0.35f, 0.15f), // ST
        FormationPos(0.65f, 0.15f) // ST
    )
)

@Composable
fun FormationTab(players: List<Player>, modifier: Modifier = Modifier, onPlayerUpdate: (Player) -> Unit = {}, onApplyFormation: (List<Player>) -> Unit = {}) {
    var draggedPlayer by remember { mutableStateOf<Player?>(null) }
    var dragGlobalPos by remember { mutableStateOf(Offset.Zero) }
    var pitchBounds by remember { mutableStateOf(androidx.compose.ui.geometry.Rect.Zero) }
    var benchBounds by remember { mutableStateOf(androidx.compose.ui.geometry.Rect.Zero) }
    
    val formations = listOf("4-3-3", "4-2-3-1", "4-4-2", "3-5-2", "5-3-2", "Custom")
    var formationExpanded by remember { mutableStateOf(false) }
    var selectedFormation by remember { mutableStateOf("Custom") }
    
    // Apply formation layout
    LaunchedEffect(selectedFormation) {
        if (selectedFormation != "Custom" && formationsMap.containsKey(selectedFormation)) {
            val layout = formationsMap[selectedFormation]!!
            val starting = players.filter { it.isStartingXI && !it.isAcademy }.take(11)
            val updatedPlayers = starting.mapIndexed { index, player ->
                if (index < layout.size) {
                    player.copy(pitchX = layout[index].x, pitchY = layout[index].y)
                } else {
                    player
                }
            }
            if (updatedPlayers.isNotEmpty()) {
                onApplyFormation(updatedPlayers)
            }
        }
    }

    Box(modifier = modifier.fillMaxWidth().padding(16.dp)) {
        Column {
            Card(modifier = Modifier.fillMaxWidth().weight(1f), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                @OptIn(ExperimentalMaterial3Api::class)
                ExposedDropdownMenuBox(
                    expanded = formationExpanded,
                    onExpandedChange = { formationExpanded = !formationExpanded },
                    modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp)
                ) {
                    OutlinedTextField(
                        value = selectedFormation,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Formation Template") },
                        modifier = Modifier.menuAnchor(androidx.compose.material3.MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(),
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = formationExpanded) }
                    )
                    ExposedDropdownMenu(
                        expanded = formationExpanded,
                        onDismissRequest = { formationExpanded = false }
                    ) {
                        formations.forEach { selectionOption ->
                            DropdownMenuItem(
                                text = { Text(selectionOption) },
                                onClick = {
                                    selectedFormation = selectionOption
                                    formationExpanded = false
                                }
                            )
                        }
                    }
                }
                
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f)
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color(0xFF2E7D32)) 
                        .border(2.dp, Color.White.copy(alpha = 0.5f), RoundedCornerShape(8.dp))
                        .onGloballyPositioned { coordinates ->
                            pitchBounds = coordinates.boundsInWindow()
                        }
                ) {
                    // Pitch Markings
                    Box(modifier = Modifier.fillMaxSize().border(1.dp, Color.White.copy(alpha = 0.3f)))
                    Box(modifier = Modifier.fillMaxWidth().height(1.dp).background(Color.White.copy(alpha = 0.3f)).align(Alignment.Center))
                    Box(modifier = Modifier.size(60.dp).border(1.dp, Color.White.copy(alpha = 0.3f), CircleShape).align(Alignment.Center))
                    Box(modifier = Modifier.size(100.dp, 60.dp).border(1.dp, Color.White.copy(alpha = 0.3f)).align(Alignment.TopCenter))
                    Box(modifier = Modifier.size(100.dp, 60.dp).border(1.dp, Color.White.copy(alpha = 0.3f)).align(Alignment.BottomCenter))
                    
                    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                        val width = maxWidth.value
                        val height = maxHeight.value
                        
                        players.filter { it.isStartingXI }.forEach { player ->
                            if (draggedPlayer?.id != player.id) {
                                Box(
                                    modifier = Modifier
                                        .offset(
                                            x = (player.pitchX * width - 24).dp, // offset by half icon width approx
                                            y = (player.pitchY * height - 32).dp
                                        )
                                        .pointerInput(Unit) {
                                            detectDragGestures(
                                                onDragStart = { offset ->
                                                    draggedPlayer = player
                                                    selectedFormation = "Custom"
                                                },
                                                onDragEnd = {
                                                    if (dragGlobalPos.y > pitchBounds.bottom) {
                                                        // Dropped outside pitch (e.g. on bench)
                                                        onPlayerUpdate(player.copy(isStartingXI = false))
                                                    } else {
                                                        // Update pitch position
                                                        val relativeX = (dragGlobalPos.x - pitchBounds.left) / pitchBounds.width
                                                        val relativeY = (dragGlobalPos.y - pitchBounds.top) / pitchBounds.height
                                                        onPlayerUpdate(player.copy(pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                                    }
                                                    draggedPlayer = null
                                                },
                                                onDragCancel = { draggedPlayer = null }
                                            ) { change, _ ->
                                                change.consume()
                                                dragGlobalPos = change.position + pitchBounds.topLeft + Offset(player.pitchX * pitchBounds.width - 24f, player.pitchY * pitchBounds.height - 32f) // Very rough approximation for seamless drag
                                            }
                                        }
                                ) {
                                    PlayerPitchIcon(player)
                                }
                            }
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Card(modifier = Modifier.fillMaxWidth().onGloballyPositioned { benchBounds = it.boundsInWindow() }, colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                Text("Bench & Reserves", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White, modifier = Modifier.padding(bottom = 8.dp))
                LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp)) {
                    items(players.filter { !it.isStartingXI && !it.isAcademy }) { player ->
                        val isDragged = draggedPlayer?.id == player.id
                        Box(
                            modifier = Modifier
                                .width(60.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(if (isDragged) MaterialTheme.colorScheme.surfaceVariant.copy(alpha=0.2f) else Color.Transparent)
                                .pointerInput(Unit) {
                                    var itemPos = Offset.Zero
                                    detectDragGestures(
                                        onDragStart = { offset -> 
                                            draggedPlayer = player
                                            selectedFormation = "Custom"
                                        },
                                        onDragEnd = {
                                            if (dragGlobalPos.y < pitchBounds.bottom && dragGlobalPos.y > pitchBounds.top &&
                                                dragGlobalPos.x > pitchBounds.left && dragGlobalPos.x < pitchBounds.right) {
                                                
                                                val startingPlayers = players.filter { it.isStartingXI && !it.isAcademy }
                                                var swapped = false
                                                if (startingPlayers.isNotEmpty()) {
                                                    val closestPlayer = startingPlayers.minByOrNull {
                                                        val px = pitchBounds.left + it.pitchX * pitchBounds.width
                                                        val py = pitchBounds.top + it.pitchY * pitchBounds.height
                                                        Math.hypot((px - dragGlobalPos.x).toDouble(), (py - dragGlobalPos.y).toDouble())
                                                    }
                                                    if (closestPlayer != null) {
                                                        val px = pitchBounds.left + closestPlayer.pitchX * pitchBounds.width
                                                        val py = pitchBounds.top + closestPlayer.pitchY * pitchBounds.height
                                                        if (Math.hypot((px - dragGlobalPos.x).toDouble(), (py - dragGlobalPos.y).toDouble()) < 150.0) {
                                                            onPlayerUpdate(closestPlayer.copy(isStartingXI = false))
                                                            onPlayerUpdate(player.copy(isStartingXI = true, pitchX = closestPlayer.pitchX, pitchY = closestPlayer.pitchY))
                                                            swapped = true
                                                        }
                                                    }
                                                }
                                                
                                                if (!swapped) {
                                                    if (startingPlayers.size < 11) {
                                                        val relativeX = (dragGlobalPos.x - pitchBounds.left) / pitchBounds.width
                                                        val relativeY = (dragGlobalPos.y - pitchBounds.top) / pitchBounds.height
                                                        onPlayerUpdate(player.copy(isStartingXI = true, pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                                    }
                                                }
                                            }
                                            draggedPlayer = null
                                        },
                                        onDragCancel = { draggedPlayer = null }
                                    ) { change, _ ->
                                        change.consume()
                                        dragGlobalPos = change.positionInWindow()
                                    }
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            if (!isDragged) {
                                PlayerPitchIcon(player)
                            } else {
                                Box(modifier = Modifier.size(48.dp).background(Color.White.copy(alpha=0.1f), CircleShape))
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun PlayerPitchIcon(player: Player) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(56.dp)) {
        if (player.isInjured) {
            Box(modifier = Modifier.background(Color.Red.copy(alpha=0.8f), RoundedCornerShape(4.dp)).padding(2.dp)) {
                Text("⚠️ Injured", fontSize = 8.sp, color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
        Box(
            modifier = Modifier
                .size(36.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primary)
                .border(1.dp, Color.White, CircleShape),
            contentAlignment = Alignment.Center
        ) {
            if (player.headshotUrl.isNotEmpty()) {
                coil.compose.AsyncImage(
                    model = player.headshotUrl,
                    contentDescription = "Player Face",
                    modifier = Modifier.fillMaxSize(),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            } else {
                Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onPrimary)
            }
            
            // Overall Rating Badge
            Box(
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .offset(x = 4.dp, y = 4.dp)
                    .clip(CircleShape)
                    .background(Color.Black)
                    .border(1.dp, Color.White, CircleShape)
                    .padding(2.dp)
            ) {
                Text(player.overall.toString(), fontSize = 8.sp, color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
        Spacer(modifier = Modifier.height(2.dp))
        Text(
            player.displayName,
            fontSize = 9.sp,
            color = Color.White,
            maxLines = 1,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.background(Color.Black.copy(alpha = 0.5f), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 1.dp)
        )
        val positions = listOfNotNull(player.primaryPosition, player.secondaryPosition).joinToString(",")
        Text(
            positions,
            fontSize = 7.sp,
            color = Color.LightGray,
            modifier = Modifier.background(Color.Black.copy(alpha = 0.5f), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp)
        )
    }
}
"""
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
        f.write(content)

rewrite()
