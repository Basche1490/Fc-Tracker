import re

def rewrite():
    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
        content = f.read()

    # 1. Update the applySmartFormation function to use multi-pass matching
    target_smart_formation = """fun applySmartFormation(players: List<Player>, formationName: String): List<Player>? {
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
}"""

    replacement_smart_formation = """fun applySmartFormation(players: List<Player>, formationName: String): List<Player>? {
    val layout = formationsMap[formationName] ?: return null
    val starting = players.filter { it.isStartingXI && !it.isAcademy }.take(11)
    
    val unassignedPlayers = starting.toMutableList()
    val assignments = mutableMapOf<FormationSlot, Player>()
    
    // Pass 1: Primary Position (Highest Overall first)
    for (slot in layout) {
        val match = unassignedPlayers.filter { it.primaryPosition in slot.roles }.maxByOrNull { it.overall }
        if (match != null) {
            assignments[slot] = match
            unassignedPlayers.remove(match)
        }
    }
    
    // Pass 2: Secondary Position
    for (slot in layout.filter { !assignments.containsKey(it) }) {
        val match = unassignedPlayers.filter { it.secondaryPosition in slot.roles }.maxByOrNull { it.overall }
        if (match != null) {
            assignments[slot] = match
            unassignedPlayers.remove(match)
        }
    }
    
    // Pass 3: Tertiary Position
    for (slot in layout.filter { !assignments.containsKey(it) }) {
        val match = unassignedPlayers.filter { it.tertiaryPosition in slot.roles }.maxByOrNull { it.overall }
        if (match != null) {
            assignments[slot] = match
            unassignedPlayers.remove(match)
        }
    }
    
    // Pass 4: Fallback (Fill remaining slots with highest overall players left)
    val remainingSlots = layout.filter { !assignments.containsKey(it) }
    remainingSlots.forEach { slot ->
        val match = unassignedPlayers.maxByOrNull { it.overall }
        if (match != null) {
            assignments[slot] = match
            unassignedPlayers.remove(match)
        }
    }
    
    return assignments.map { (slot, player) ->
        player.copy(pitchX = slot.x, pitchY = slot.y)
    }
}"""
    content = content.replace(target_smart_formation, replacement_smart_formation)

    # 2. Fix positionInWindow -> positionInRoot
    content = content.replace("positionInWindow()", "positionInRoot()")
    content = content.replace("boundsInWindow()", "boundsInRoot()")

    with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "w") as f:
        f.write(content)

rewrite()
