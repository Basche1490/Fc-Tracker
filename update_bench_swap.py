import re

with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
    content = f.read()

# Update signature
old_sig = "fun FormationTab(players: List<Player>, modifier: Modifier = Modifier, onPlayerUpdate: (Player) -> Unit = {}, onApplyFormation: (List<Player>) -> Unit = {}) {"
new_sig = "fun FormationTab(players: List<Player>, modifier: Modifier = Modifier, onPlayerUpdate: (Player) -> Unit = {}, onApplyFormation: (List<Player>) -> Unit = {}, onSwapPlayers: (String, String) -> Unit = { _, _ -> }) {"
content = content.replace(old_sig, new_sig)

# Add benchPositions
old_state = "var selectedFormation by remember { mutableStateOf(\"Custom\") }"
new_state = """var selectedFormation by remember { mutableStateOf("Custom") }
    val benchPositions = remember { androidx.compose.runtime.mutableStateMapOf<String, androidx.compose.ui.geometry.Offset>() }"""
content = content.replace(old_state, new_state)

# Update onGloballyPositioned for bench Box
old_globally = ".onGloballyPositioned { myGlobalPos = it.positionInRoot() }"
new_globally = """.onGloballyPositioned { 
                                        myGlobalPos = it.positionInRoot() 
                                        benchPositions[player.id] = androidx.compose.ui.geometry.Offset(myGlobalPos.x + it.size.width / 2f, myGlobalPos.y + it.size.height / 2f)
                                    }"""
content = content.replace(old_globally, new_globally)

# Add the else block in bench onDragEnd
old_end = """                                                            if (startingPlayers.size < 11) {
                                                                val relativeX = (finalGlobalX - pitchBounds.left) / pitchBounds.width
                                                                val relativeY = (finalGlobalY - pitchBounds.top) / pitchBounds.height
                                                                onPlayerUpdate(player.copy(isStartingXI = true, pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                                            }
                                                        }
                                                    }
                                                    draggedPlayer = null"""

new_end = """                                                            if (startingPlayers.size < 11) {
                                                                val relativeX = (finalGlobalX - pitchBounds.left) / pitchBounds.width
                                                                val relativeY = (finalGlobalY - pitchBounds.top) / pitchBounds.height
                                                                onPlayerUpdate(player.copy(isStartingXI = true, pitchX = relativeX.coerceIn(0f, 1f), pitchY = relativeY.coerceIn(0f, 1f)))
                                                            }
                                                        }
                                                    } else {
                                                        val closestBenchPlayer = benchPositions.entries.minByOrNull {
                                                            kotlin.math.hypot((it.value.x - finalGlobalX).toDouble(), (it.value.y - finalGlobalY).toDouble())
                                                        }
                                                        if (closestBenchPlayer != null && closestBenchPlayer.key != player.id && kotlin.math.hypot((closestBenchPlayer.value.x - finalGlobalX).toDouble(), (closestBenchPlayer.value.y - finalGlobalY).toDouble()) < 150.0) {
                                                            onSwapPlayers(player.id, closestBenchPlayer.key)
                                                        }
                                                    }
                                                    draggedPlayer = null"""
content = content.replace(old_end, new_end)

with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
    f.write(content)

