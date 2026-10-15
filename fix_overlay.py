import re

def rewrite():
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
        content = f.read()

    target = "    }\n}\n\n@Composable\nfun PlayerPitchIcon"
    
    replacement = """    }

    if (draggedPlayer != null) {
        androidx.compose.ui.window.Popup(
            alignment = Alignment.TopStart,
            offset = androidx.compose.ui.unit.IntOffset(
                x = dragGlobalPos.x.toInt() - 75, // Adjust for center
                y = dragGlobalPos.y.toInt() - 75
            )
        ) {
            Box(modifier = Modifier.zIndex(100f)) {
                PlayerPitchIcon(draggedPlayer!!)
            }
        }
    }
}

@Composable
fun PlayerPitchIcon"""
    
    content = content.replace(target, replacement)

    # Let's also fix the drag logic for the pitch players
    target2 = """                                            detectDragGestures(
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
                                            }"""

    replacement2 = """                                            detectDragGestures(
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
                                            }"""
                                            
    content = content.replace(target2, replacement2)
                                            
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
        f.write(content)

rewrite()
