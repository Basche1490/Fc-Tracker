import re

def rewrite():
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
        content = f.read()

    # For pitch players:
    target1 = """                                        .pointerInput(Unit) {
                                            detectDragGestures(
                                                onDragStart = { offset ->
                                                    draggedPlayer = player
                                                    selectedFormation = "Custom"
                                                },
                                                onDragEnd = {
                                                    if (dragGlobalPos.y > pitchBounds.bottom || dragGlobalPos.y < pitchBounds.top) {
                                                        onPlayerUpdate(player.copy(isStartingXI = false))
                                                    } else {
                                                        val relativeX = (dragGlobalPos.x - pitchBounds.left) / pitchBounds.width
                                                        val relativeY = (dragGlobalPos.y - pitchBounds.top) / pitchBounds.height
                                                        onPlayerUpdate(player.copy(pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                                    }
                                                    draggedPlayer = null
                                                },
                                                onDragCancel = { draggedPlayer = null }
                                            ) { change, _ ->
                                                change.consume()
                                                dragGlobalPos = change.positionInWindow()
                                            }
                                        }"""

    replacement1 = """                                        .onGloballyPositioned { coordinates ->
                                            if (draggedPlayer?.id == player.id && dragGlobalPos == Offset.Zero) {
                                                dragGlobalPos = coordinates.positionInWindow()
                                            }
                                        }
                                        .pointerInput(Unit) {
                                            var itemPos = Offset.Zero
                                            detectDragGestures(
                                                onDragStart = { offset ->
                                                    draggedPlayer = player
                                                    selectedFormation = "Custom"
                                                },
                                                onDragEnd = {
                                                    if (dragGlobalPos.y > pitchBounds.bottom || dragGlobalPos.y < pitchBounds.top) {
                                                        onPlayerUpdate(player.copy(isStartingXI = false))
                                                    } else {
                                                        val relativeX = (dragGlobalPos.x - pitchBounds.left) / pitchBounds.width
                                                        val relativeY = (dragGlobalPos.y - pitchBounds.top) / pitchBounds.height
                                                        onPlayerUpdate(player.copy(pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                                    }
                                                    draggedPlayer = null
                                                },
                                                onDragCancel = { draggedPlayer = null }
                                            ) { change, dragAmount ->
                                                change.consume()
                                                dragGlobalPos += dragAmount
                                            }
                                        }"""
    content = content.replace(target1, replacement1)

    # For bench players:
    target2 = """                                .pointerInput(Unit) {
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
                                }"""

    replacement2 = """                                .onGloballyPositioned { coordinates ->
                                    if (draggedPlayer?.id == player.id && dragGlobalPos == Offset.Zero) {
                                        dragGlobalPos = coordinates.positionInWindow()
                                    }
                                }
                                .pointerInput(Unit) {
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
                                    ) { change, dragAmount ->
                                        change.consume()
                                        dragGlobalPos += dragAmount
                                    }
                                }"""
    content = content.replace(target2, replacement2)

    # We also need to set dragGlobalPos = Offset.Zero when we clear draggedPlayer
    content = content.replace("draggedPlayer = null", "draggedPlayer = null\ndragGlobalPos = Offset.Zero")
    
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
        f.write(content)

rewrite()
