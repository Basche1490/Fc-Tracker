import re

with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
    content = f.read()

# Extract from "LazyRow..." to the matching closing brace.
start_str = "LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp)) {"
end_str_lookaround = "} // End LazyRow" # Just an idea, but let's do simple matching

start_idx = content.find(start_str)
if start_idx != -1:
    brace_count = 0
    end_idx = -1
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    if end_idx != -1:
        old_bench = content[start_idx:end_idx]
        
        # Now create new bench
        new_bench = """Column(verticalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp)) {
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
                                        .alpha(if (isDragged) 0f else 1f),
                                    contentAlignment = Alignment.Center
                                ) {
                                    PlayerPitchIcon(player)
                                }
                            }
                            for (i in 0 until (6 - rowPlayers.size)) {
                                Spacer(modifier = Modifier.weight(1f))
                            }
                        }
                    }
                }"""
                
        content = content[:start_idx] + new_bench + content[end_idx:]
        with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
            f.write(content)
        print("Success")
    else:
        print("Could not find matching brace")
else:
    print("Could not find LazyRow")
