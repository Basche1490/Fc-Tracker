cat << 'INNER_EOF' > app/src/main/java/com/example/ui/screens/FormationTab.kt
package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.ui.layout.boundsInRoot
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import com.example.Player

@Composable
fun FormationTab(players: List<Player>, modifier: Modifier = Modifier, onPlayerUpdate: (Player) -> Unit = {}) {
    var draggedPlayer by remember { mutableStateOf<Player?>(null) }
    var dragPosition by remember { mutableStateOf(Offset.Zero) }
    var pitchBounds by remember { mutableStateOf(androidx.compose.ui.geometry.Rect.Zero) }
    var dragOffset by remember { mutableStateOf(Offset.Zero) }
    
    val formations = listOf("4-3-3", "4-2-3-1", "4-4-2", "3-5-2", "5-3-2", "4-1-2-1-2", "3-4-3", "Custom")
    var formationExpanded by remember { mutableStateOf(false) }
    var selectedFormation by remember { mutableStateOf(formations[0]) }
    val density = androidx.compose.ui.platform.LocalDensity.current

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
                        label = { Text("Formation") },
                        modifier = Modifier.menuAnchor(MenuAnchorType.PrimaryNotEditable, true).fillMaxWidth(),
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
                            pitchBounds = coordinates.boundsInRoot()
                        }
                ) {
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
                                            x = (player.pitchX * width - 16).dp,
                                            y = (player.pitchY * height - 16).dp
                                        )
                                        .pointerInput(Unit) {
                                            detectDragGestures(
                                                onDragStart = { },
                                                onDragEnd = { },
                                                onDragCancel = { }
                                            ) { change, dragAmount ->
                                                change.consume()
                                                val densityScale = density.density
                                                val newX = (player.pitchX * width + dragAmount.x / densityScale) / width
                                                val newY = (player.pitchY * height + dragAmount.y / densityScale) / height
                                                onPlayerUpdate(player.copy(pitchX = newX.coerceIn(0f, 1f), pitchY = newY.coerceIn(0f, 1f)))
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
            
            Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                Text("Bench & Reserves", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White, modifier = Modifier.padding(bottom = 8.dp))
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(players.filter { !it.isStartingXI && !it.isAcademy }) { player ->
                        val isDragged = draggedPlayer?.id == player.id
                        Box(
                            modifier = Modifier
                                .width(80.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(if (isDragged) MaterialTheme.colorScheme.surfaceVariant.copy(alpha=0.5f) else MaterialTheme.colorScheme.surfaceVariant)
                                .padding(8.dp)
                                .onGloballyPositioned { coordinates ->
                                    if (isDragged && dragPosition == Offset.Zero) {
                                        dragPosition = coordinates.positionInRoot()
                                    }
                                }
                                .pointerInput(Unit) {
                                    detectDragGestures(
                                        onDragStart = { 
                                            draggedPlayer = player
                                            dragOffset = Offset.Zero
                                        },
                                        onDragEnd = {
                                            val globalDropY = dragPosition.y + dragOffset.y
                                            val globalDropX = dragPosition.x + dragOffset.x
                                            if (globalDropY < pitchBounds.bottom && globalDropY > pitchBounds.top &&
                                                globalDropX > pitchBounds.left && globalDropX < pitchBounds.right) {
                                                val relativeX = (globalDropX - pitchBounds.left) / pitchBounds.width
                                                val relativeY = (globalDropY - pitchBounds.top) / pitchBounds.height
                                                onPlayerUpdate(player.copy(isStartingXI = true, pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                            }
                                            draggedPlayer = null
                                            dragOffset = Offset.Zero
                                            dragPosition = Offset.Zero
                                        },
                                        onDragCancel = {
                                            draggedPlayer = null
                                            dragOffset = Offset.Zero
                                            dragPosition = Offset.Zero
                                        }
                                    ) { change, dragAmount ->
                                        change.consume()
                                        dragOffset += dragAmount
                                    }
                                },
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Box(
                                    modifier = Modifier
                                        .size(24.dp)
                                        .clip(CircleShape)
                                        .background(MaterialTheme.colorScheme.secondary),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(player.overall.toString(), fontSize = 10.sp, color = MaterialTheme.colorScheme.onSecondary, fontWeight = FontWeight.Bold)
                                }
                                Text(
                                    player.lastName,
                                    fontSize = 10.sp,
                                    color = Color.White,
                                    maxLines = 1
                                )
                                Button(
                                    onClick = { onPlayerUpdate(player.copy(isStartingXI = true, pitchX = 0.5f, pitchY = 0.9f)) },
                                    contentPadding = PaddingValues(0.dp),
                                    modifier = Modifier.height(20.dp).padding(top = 4.dp)
                                ) {
                                    Text("Start", fontSize = 8.sp)
                                }
                            }
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(80.dp))
        }

        draggedPlayer?.let { player ->
            Box(
                modifier = Modifier
                    .offset(
                        x = with(androidx.compose.ui.platform.LocalDensity.current) { dragOffset.x.toDp() + (dragPosition.x.toDp() - 16.dp) },
                        y = with(androidx.compose.ui.platform.LocalDensity.current) { dragOffset.y.toDp() + (dragPosition.y.toDp() - 80.dp) } 
                    )
                    .zIndex(10f)
            ) {
                PlayerPitchIcon(player)
            }
        }
    }
}

@Composable
fun PlayerPitchIcon(player: Player) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        if (player.isInjured) {
            Box(modifier = Modifier.background(Color.Red.copy(alpha=0.8f), RoundedCornerShape(4.dp)).padding(2.dp)) {
                Text("⚠️ Injured", fontSize = 8.sp, color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
        Box(
            modifier = Modifier
                .size(32.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primary),
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
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.background(Color.Black.copy(alpha = 0.6f), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp)) {
            Text(
                "\${player.lastName} | \${player.overall}",
                fontSize = 10.sp,
                color = Color.White
            )
        }
        val positions = listOfNotNull(player.primaryPosition, player.secondaryPosition, player.tertiaryPosition).joinToString(", ")
        Text(
            positions,
            fontSize = 8.sp,
            color = Color.LightGray,
            modifier = Modifier.background(Color.Black.copy(alpha = 0.6f), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp)
        )
    }
}
INNER_EOF
