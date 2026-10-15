import re

def rewrite():
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
        content = f.read()

    # 1. Update the states
    target_states = """    var draggedPlayer by remember { mutableStateOf<Player?>(null) }
    var dragStartGlobalPosition by remember { mutableStateOf(Offset.Zero) }
    var dragOffset by remember { mutableStateOf(Offset.Zero) }"""
    
    replacement_states = """    var draggedPlayer by remember { mutableStateOf<Player?>(null) }
    var dragCenterGlobal by remember { mutableStateOf(Offset.Zero) }
    val localDensity = androidx.compose.ui.platform.LocalDensity.current"""
    
    content = content.replace(target_states, replacement_states)

    # 2. Update pitch drag logic
    target_pitch_drag = """                                            onDragStart = { offset ->
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
                                        }"""
                                        
    replacement_pitch_drag = """                                            onDragStart = { offset ->
                                                draggedPlayer = player
                                                dragCenterGlobal = Offset(myGlobalPos.x + offset.x, myGlobalPos.y + offset.y)
                                                selectedFormation = "Custom"
                                            },
                                            onDragEnd = {
                                                val finalGlobalY = dragCenterGlobal.y
                                                val finalGlobalX = dragCenterGlobal.x
                                                
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
                                            dragCenterGlobal += dragAmount
                                        }"""
    content = content.replace(target_pitch_drag, replacement_pitch_drag)

    # 3. Update bench drag logic
    target_bench_drag = """                                        onDragStart = { offset -> 
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
                                    }"""
                                    
    replacement_bench_drag = """                                        onDragStart = { offset -> 
                                            draggedPlayer = player
                                            dragCenterGlobal = Offset(myGlobalPos.x + offset.x, myGlobalPos.y + offset.y)
                                            selectedFormation = "Custom"
                                        },
                                        onDragEnd = {
                                            val finalGlobalY = dragCenterGlobal.y
                                            val finalGlobalX = dragCenterGlobal.x
                                            
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
                                        dragCenterGlobal += dragAmount
                                    }"""
    content = content.replace(target_bench_drag, replacement_bench_drag)

    # 4. Update the overlay rendering
    target_overlay = """        // Overlay for Dragged Player (Tracks 1:1 with finger)
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
        }"""
        
    replacement_overlay = """        // Overlay for Dragged Player (Snaps center perfectly to finger)
        if (draggedPlayer != null) {
            val iconCenterOffsetX = with(localDensity) { 30.dp.toPx() }
            val iconCenterOffsetY = with(localDensity) { 45.dp.toPx() } // Approx half of total icon height
            
            val localX = dragCenterGlobal.x - rootPos.x - iconCenterOffsetX
            val localY = dragCenterGlobal.y - rootPos.y - iconCenterOffsetY
            
            Box(
                modifier = Modifier
                    .offset { IntOffset(localX.roundToInt(), localY.roundToInt()) }
                    .zIndex(100f)
            ) {
                PlayerPitchIcon(draggedPlayer!!)
            }
        }"""
    content = content.replace(target_overlay, replacement_overlay)

    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
        f.write(content)

rewrite()
