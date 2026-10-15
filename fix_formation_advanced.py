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
import androidx.compose.ui.layout.boundsInWindow
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInWindow
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import com.example.Player
import kotlin.math.hypot
import kotlin.math.roundToInt

data class FormationSlot(val x: Float, val y: Float, val roles: List<String>)

val formationsMap = mapOf(
    "4-3-3" to listOf(
        FormationSlot(0.5f, 0.85f, listOf("GK")),
        FormationSlot(0.15f, 0.65f, listOf("LB", "LWB")),
        FormationSlot(0.35f, 0.7f, listOf("CB")),
        FormationSlot(0.65f, 0.7f, listOf("CB")),
        FormationSlot(0.85f, 0.65f, listOf("RB", "RWB")),
        FormationSlot(0.25f, 0.45f, listOf("CM", "CDM", "CAM")),
        FormationSlot(0.5f, 0.5f, listOf("CM", "CDM", "CAM")),
        FormationSlot(0.75f, 0.45f, listOf("CM", "CDM", "CAM")),
        FormationSlot(0.2f, 0.2f, listOf("LW", "LM", "LF")),
        FormationSlot(0.5f, 0.15f, listOf("ST", "CF")),
        FormationSlot(0.8f, 0.2f, listOf("RW", "RM", "RF"))
    ),
    "4-2-3-1" to listOf(
        FormationSlot(0.5f, 0.85f, listOf("GK")),
        FormationSlot(0.15f, 0.65f, listOf("LB", "LWB")),
        FormationSlot(0.35f, 0.7f, listOf("CB")),
        FormationSlot(0.65f, 0.7f, listOf("CB")),
        FormationSlot(0.85f, 0.65f, listOf("RB", "RWB")),
        FormationSlot(0.35f, 0.55f, listOf("CDM", "CM")),
        FormationSlot(0.65f, 0.55f, listOf("CDM", "CM")),
        FormationSlot(0.2f, 0.35f, listOf("CAM", "LM", "LW")),
        FormationSlot(0.5f, 0.3f, listOf("CAM", "CM")),
        FormationSlot(0.8f, 0.35f, listOf("CAM", "RM", "RW")),
        FormationSlot(0.5f, 0.15f, listOf("ST", "CF"))
    ),
    "4-4-2" to listOf(
        FormationSlot(0.5f, 0.85f, listOf("GK")),
        FormationSlot(0.15f, 0.65f, listOf("LB", "LWB")),
        FormationSlot(0.35f, 0.7f, listOf("CB")),
        FormationSlot(0.65f, 0.7f, listOf("CB")),
        FormationSlot(0.85f, 0.65f, listOf("RB", "RWB")),
        FormationSlot(0.15f, 0.45f, listOf("LM", "LW")),
        FormationSlot(0.35f, 0.45f, listOf("CM", "CDM")),
        FormationSlot(0.65f, 0.45f, listOf("CM", "CDM")),
        FormationSlot(0.85f, 0.45f, listOf("RM", "RW")),
        FormationSlot(0.35f, 0.15f, listOf("ST", "CF")),
        FormationSlot(0.65f, 0.15f, listOf("ST", "CF"))
    ),
    "3-5-2" to listOf(
        FormationSlot(0.5f, 0.85f, listOf("GK")),
        FormationSlot(0.25f, 0.75f, listOf("CB")),
        FormationSlot(0.5f, 0.75f, listOf("CB")),
        FormationSlot(0.75f, 0.75f, listOf("CB")),
        FormationSlot(0.15f, 0.45f, listOf("LWB", "LM")),
        FormationSlot(0.35f, 0.55f, listOf("CDM", "CM")),
        FormationSlot(0.5f, 0.4f, listOf("CAM", "CM")),
        FormationSlot(0.65f, 0.55f, listOf("CDM", "CM")),
        FormationSlot(0.85f, 0.45f, listOf("RWB", "RM")),
        FormationSlot(0.35f, 0.15f, listOf("ST", "CF")),
        FormationSlot(0.65f, 0.15f, listOf("ST", "CF"))
    ),
    "5-3-2" to listOf(
        FormationSlot(0.5f, 0.85f, listOf("GK")),
        FormationSlot(0.1f, 0.65f, listOf("LWB", "LB")),
        FormationSlot(0.3f, 0.75f, listOf("CB")),
        FormationSlot(0.5f, 0.75f, listOf("CB")),
        FormationSlot(0.7f, 0.75f, listOf("CB")),
        FormationSlot(0.9f, 0.65f, listOf("RWB", "RB")),
        FormationSlot(0.25f, 0.45f, listOf("CM", "CDM")),
        FormationSlot(0.5f, 0.45f, listOf("CM", "CAM")),
        FormationSlot(0.75f, 0.45f, listOf("CM", "CDM")),
        FormationSlot(0.35f, 0.15f, listOf("ST", "CF")),
        FormationSlot(0.65f, 0.15f, listOf("ST", "CF"))
    )
)

fun applySmartFormation(players: List<Player>, formationName: String): List<Player>? {
    val layout = formationsMap[formationName] ?: return null
    val starting = players.filter { it.isStartingXI && !it.isAcademy }.take(11)
    
    val unassigned = starting.toMutableList()
    val updatedPlayers = mutableListOf<Player>()
    
    for (slot in layout) {
        var bestFit: Player? = null
        
        // 1. Primary Position Match
        bestFit = unassigned.firstOrNull { it.primaryPosition in slot.roles }
        
        // 2. Secondary Position Match
        if (bestFit == null) {
            bestFit = unassigned.firstOrNull { it.secondaryPosition in slot.roles }
        }
        
        // 3. Tertiary Position Match
        if (bestFit == null) {
            bestFit = unassigned.firstOrNull { it.tertiaryPosition in slot.roles }
        }
        
        // 4. Fallback: Highest Overall
        if (bestFit == null) {
            bestFit = unassigned.maxByOrNull { it.overall }
        }
        
        if (bestFit != null) {
            unassigned.remove(bestFit)
            updatedPlayers.add(bestFit.copy(pitchX = slot.x, pitchY = slot.y))
        }
    }
    
    return updatedPlayers
}

@Composable
fun FormationTab(players: List<Player>, modifier: Modifier = Modifier, onPlayerUpdate: (Player) -> Unit = {}, onApplyFormation: (List<Player>) -> Unit = {}) {
    var draggedPlayer by remember { mutableStateOf<Player?>(null) }
    var dragStartGlobalPosition by remember { mutableStateOf(Offset.Zero) }
    var dragOffset by remember { mutableStateOf(Offset.Zero) }
    
    var rootPos by remember { mutableStateOf(Offset.Zero) }
    var pitchBounds by remember { mutableStateOf(androidx.compose.ui.geometry.Rect.Zero) }
    
    val formations = listOf("4-3-3", "4-2-3-1", "4-4-2", "3-5-2", "5-3-2", "Custom")
    var formationExpanded by remember { mutableStateOf(false) }
    
    // Remember initial load to trigger 4-3-3 default layout
    var initialLoadDone by remember { mutableStateOf(false) }
    var selectedFormation by remember { mutableStateOf("4-3-3") }
    
    LaunchedEffect(selectedFormation, initialLoadDone) {
        if (!initialLoadDone) {
            initialLoadDone = true
            val updated = applySmartFormation(players, "4-3-3")
            if (updated != null) {
                onApplyFormation(updated)
            }
        } else if (selectedFormation != "Custom") {
            val updated = applySmartFormation(players, selectedFormation)
            if (updated != null) {
                onApplyFormation(updated)
            }
        }
    }

    Box(modifier = modifier.fillMaxWidth().padding(16.dp).onGloballyPositioned { rootPos = it.positionInWindow() }) {
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
                            val isDragged = draggedPlayer?.id == player.id
                            var myGlobalPos by remember { mutableStateOf(Offset.Zero) }
                            
                            Box(
                                modifier = Modifier
                                    .offset(
                                        x = (player.pitchX * width - 30).dp, // Adjust offset to center icon (approx 60dp width)
                                        y = (player.pitchY * height - 30).dp
                                    )
                                    .onGloballyPositioned { myGlobalPos = it.positionInWindow() }
                                    .pointerInput(Unit) {
                                        detectDragGestures(
                                            onDragStart = { offset ->
                                                draggedPlayer = player
                                                dragStartGlobalPosition = myGlobalPos
                                                dragOffset = Offset.Zero
                                                selectedFormation = "Custom"
                                            },
                                            onDragEnd = {
                                                val finalGlobalY = dragStartGlobalPosition.y + dragOffset.y + 30f // Add roughly half icon height for center drop point
                                                val finalGlobalX = dragStartGlobalPosition.x + dragOffset.x + 30f
                                                
                                                if (finalGlobalY > pitchBounds.bottom || finalGlobalY < pitchBounds.top) {
                                                    onPlayerUpdate(player.copy(isStartingXI = false))
                                                } else {
                                                    val relativeX = (finalGlobalX - pitchBounds.left) / pitchBounds.width
                                                    val relativeY = (finalGlobalY - pitchBounds.top) / pitchBounds.height
                                                    onPlayerUpdate(player.copy(pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                                }
                                                draggedPlayer = null
                                            },
                                            onDragCancel = { draggedPlayer = null }
                                        ) { change, dragAmount ->
                                            change.consume()
                                            dragOffset += dragAmount
                                        }
                                    }
                                    .alpha(if (isDragged) 0f else 1f)
                            ) {
                                PlayerPitchIcon(player)
                            }
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                Text("Bench & Reserves", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White, modifier = Modifier.padding(bottom = 8.dp, start = 8.dp, top = 8.dp))
                LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp)) {
                    items(players.filter { !it.isStartingXI && !it.isAcademy }) { player ->
                        val isDragged = draggedPlayer?.id == player.id
                        var myGlobalPos by remember { mutableStateOf(Offset.Zero) }
                        
                        Box(
                            modifier = Modifier
                                .width(60.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(Color.Transparent)
                                .onGloballyPositioned { myGlobalPos = it.positionInWindow() }
                                .pointerInput(Unit) {
                                    detectDragGestures(
                                        onDragStart = { offset -> 
                                            draggedPlayer = player
                                            dragStartGlobalPosition = myGlobalPos
                                            dragOffset = Offset.Zero
                                            selectedFormation = "Custom"
                                        },
                                        onDragEnd = {
                                            val finalGlobalY = dragStartGlobalPosition.y + dragOffset.y + 30f
                                            val finalGlobalX = dragStartGlobalPosition.x + dragOffset.x + 30f
                                            
                                            if (finalGlobalY < pitchBounds.bottom && finalGlobalY > pitchBounds.top &&
                                                finalGlobalX > pitchBounds.left && finalGlobalX < pitchBounds.right) {
                                                
                                                val startingPlayers = players.filter { it.isStartingXI && !it.isAcademy }
                                                var swapped = false
                                                if (startingPlayers.isNotEmpty()) {
                                                    val closestPlayer = startingPlayers.minByOrNull {
                                                        val px = pitchBounds.left + it.pitchX * pitchBounds.width
                                                        val py = pitchBounds.top + it.pitchY * pitchBounds.height
                                                        hypot((px - finalGlobalX).toDouble(), (py - finalGlobalY).toDouble())
                                                    }
                                                    if (closestPlayer != null) {
                                                        val px = pitchBounds.left + closestPlayer.pitchX * pitchBounds.width
                                                        val py = pitchBounds.top + closestPlayer.pitchY * pitchBounds.height
                                                        if (hypot((px - finalGlobalX).toDouble(), (py - finalGlobalY).toDouble()) < 150.0) {
                                                            onPlayerUpdate(closestPlayer.copy(isStartingXI = false))
                                                            onPlayerUpdate(player.copy(isStartingXI = true, pitchX = closestPlayer.pitchX, pitchY = closestPlayer.pitchY))
                                                            swapped = true
                                                        }
                                                    }
                                                }
                                                
                                                if (!swapped) {
                                                    if (startingPlayers.size < 11) {
                                                        val relativeX = (finalGlobalX - pitchBounds.left) / pitchBounds.width
                                                        val relativeY = (finalGlobalY - pitchBounds.top) / pitchBounds.height
                                                        onPlayerUpdate(player.copy(isStartingXI = true, pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                                    }
                                                }
                                            }
                                            draggedPlayer = null
                                        },
                                        onDragCancel = { draggedPlayer = null }
                                    ) { change, dragAmount ->
                                        change.consume()
                                        dragOffset += dragAmount
                                    }
                                }
                                .alpha(if (isDragged) 0f else 1f),
                            contentAlignment = Alignment.Center
                        ) {
                            PlayerPitchIcon(player)
                        }
                    }
                }
            }
        }

        // Overlay for Dragged Player (Tracks 1:1 with finger)
        if (draggedPlayer != null) {
            val localX = dragStartGlobalPosition.x - rootPos.x + dragOffset.x
            val localY = dragStartGlobalPosition.y - rootPos.y + dragOffset.y
            
            Box(
                modifier = Modifier
                    .offset { IntOffset(localX.roundToInt(), localY.roundToInt()) }
                    .zIndex(100f)
            ) {
                PlayerPitchIcon(draggedPlayer!!)
            }
        }
    }
}

@Composable
fun PlayerPitchIcon(player: Player) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(60.dp)) {
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
        }
        Spacer(modifier = Modifier.height(4.dp))
        
        // Name and Overall horizontally aligned
        Row(
            modifier = Modifier.background(Color.Black.copy(alpha = 0.7f), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                player.displayName,
                fontSize = 9.sp,
                color = Color.White,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.weight(1f, fill = false)
            )
            Spacer(modifier = Modifier.width(2.dp))
            Text(
                player.overall.toString(),
                fontSize = 9.sp,
                color = Color(0xFFFDD835), // Gold color for overall
                fontWeight = FontWeight.Bold
            )
        }
        Spacer(modifier = Modifier.height(2.dp))
        
        // Positions
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
