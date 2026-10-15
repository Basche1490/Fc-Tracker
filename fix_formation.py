import re

with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
    content = f.read()

# Fix pointerInput(Unit) -> pointerInput(player)
content = content.replace("pointerInput(Unit) {\n                                        detectDragGestures(", "pointerInput(player) {\n                                        detectDragGestures(")
content = content.replace("pointerInput(Unit) {\n                                    detectDragGestures(", "pointerInput(player) {\n                                    detectDragGestures(")


# Fix LazyRow bench to Column chunked
bench_old = """
                LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp)) {
                    items(players.filter { !it.isStartingXI && !it.isAcademy }) { player ->
                        val isDragged = draggedPlayer?.id == player.id
                        var myGlobalPos by remember { mutableStateOf(Offset.Zero) }
                        
                        Box(
                            modifier = Modifier
                                .width(60.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(Color.Transparent)
                                .onGloballyPositioned { myGlobalPos = it.positionInRoot() }
                                .pointerInput(player) {
                                    detectDragGestures(
                                        onDragStart = { offset -> 
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
                                    }
                                }
                                .alpha(if (isDragged) 0f else 1f)
                        ) {
                            PlayerPitchIcon(player)
                        }
                    }
                }
"""

bench_new = """
                Column(verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp)) {
                    val benchPlayers = players.filter { !it.isStartingXI && !it.isAcademy }
                    benchPlayers.chunked(6).forEach { rowPlayers ->
                        Row(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.fillMaxWidth()) {
                            rowPlayers.forEach { player ->
                                val isDragged = draggedPlayer?.id == player.id
                                var myGlobalPos by remember { mutableStateOf(Offset.Zero) }
                                
                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(Color.Transparent)
                                        .onGloballyPositioned { myGlobalPos = it.positionInRoot() }
                                        .pointerInput(player) {
                                            detectDragGestures(
                                                onDragStart = { offset -> 
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
                                            }
                                        }
                                        .alpha(if (isDragged) 0f else 1f)
                                ) {
                                    PlayerPitchIcon(player)
                                }
                            }
                            // Fill remaining slots in the row with dummy spacers to maintain grid alignment
                            for (i in 0 until (6 - rowPlayers.size)) {
                                Spacer(modifier = Modifier.weight(1f))
                            }
                        }
                    }
                }
"""

if bench_old.strip() in content:
    content = content.replace(bench_old.strip(), bench_new.strip())
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
        f.write(content)
    print("Replaced bench")
else:
    print("Failed to replace bench")

