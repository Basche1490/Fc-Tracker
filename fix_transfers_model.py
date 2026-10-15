import re

with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

# Add mapEafcPlayerToPlayer function
map_function = """
    private fun mapEafcPlayerToPlayer(eafcPlayer: EafcPlayer): Player {
        val idStr = eafcPlayer.id.toString()
        var headshotUrl = ""
        if (idStr.isNotEmpty()) {
            val paddedId = idStr.padStart(6, '0')
            headshotUrl = "https://cdn.sofifa.net/players/${paddedId.substring(0,3)}/${paddedId.substring(3,6)}/24_120.png"
        }
        val altPos = eafcPlayer.alternatePositions.split(",")
        val secPos = altPos.getOrNull(0)?.trim() ?: ""
        val tertPos = altPos.getOrNull(1)?.trim() ?: ""

        val rawBirthdate = eafcPlayer.birthdate
        var birthDateStr = rawBirthdate.split(" ")[0]
        try {
            val parts = birthDateStr.split("/")
            if (parts.size == 3) {
                birthDateStr = "${parts[2]}-${parts[0].padStart(2, '0')}-${parts[1].padStart(2, '0')}"
            }
        } catch(e: Exception) {}
        val birthYear = try { birthDateStr.split("-")[0].toInt() } catch(e: Exception) { 2000 }
        val ageCalc = _state.value.startYear - birthYear
        
        return Player(
            name = eafcPlayer.name,
            nickname = eafcPlayer.commonName.takeIf { it.isNotBlank() },
            primaryPosition = eafcPlayer.position,
            secondaryPosition = secPos.takeIf { it.isNotBlank() },
            tertiaryPosition = tertPos.takeIf { it.isNotBlank() },
            age = ageCalc,
            startingOverall = eafcPlayer.rating,
            overall = eafcPlayer.rating,
            potential = eafcPlayer.potential,
            valueM = eafcPlayer.value,
            wageK = eafcPlayer.wage,
            nationality = eafcPlayer.nationality,
            birthDate = birthDateStr,
            height = eafcPlayer.height,
            weight = eafcPlayer.weight,
            preferredFoot = eafcPlayer.preferredFoot,
            weakFoot = eafcPlayer.weakFoot,
            headshotUrl = headshotUrl
        )
    }
"""

if "private fun mapEafcPlayerToPlayer" not in content:
    content = content.replace("fun addTransferLog(log: TransferLog) {", map_function + "\n    fun addTransferLog(log: TransferLog) {")

old_addTransferLog = """    fun addTransferLog(log: TransferLog) {
        _state.update { state ->
            val updatedPlayers = state.players.map { player ->
                if (player.name == log.playerName || player.displayName == log.playerName) {
                    when (log.type) {
                        "Out (Permanent)" -> player.copy(status = "Sold")
                        "Out (Loan)" -> player.copy(status = "Loaned Out", isLoanedOut = true, isStartingXI = false)
                        "In (Loan)" -> player.copy(isLoanedIn = true)
                        else -> player
                    }
                } else {
                    player
                }
            }
            state.copy(transfers = state.transfers + log, players = updatedPlayers)
        }
    }"""

new_addTransferLog = """    fun addTransferLog(log: TransferLog) {
        _state.update { state ->
            val existingPlayer = state.players.find { it.name == log.playerName || it.displayName == log.playerName }
            val newPlayers = state.players.toMutableList()
            if (existingPlayer != null) {
                val index = newPlayers.indexOf(existingPlayer)
                when (log.type) {
                    "Out (Permanent)" -> newPlayers[index] = existingPlayer.copy(status = "Sold", isStartingXI = false)
                    "Out (Loan)" -> newPlayers[index] = existingPlayer.copy(status = "Loaned Out", isLoanedOut = true, isStartingXI = false)
                    "In (Loan)" -> newPlayers[index] = existingPlayer.copy(isLoanedIn = true, status = "Active", isLoanedOut = false)
                    "In (Permanent)", "Free Agent Sign" -> newPlayers[index] = existingPlayer.copy(isLoanedIn = false, isLoanedOut = false, status = "Active")
                }
            } else if (log.type.startsWith("In") || log.type == "Free Agent Sign") {
                val eafcMatch = allEafcPlayers.find { it.name == log.playerName || it.commonName == log.playerName || "${it.commonName} (${it.name})" == log.playerName }
                if (eafcMatch != null) {
                    val p = mapEafcPlayerToPlayer(eafcMatch).copy(
                        status = "Active",
                        isLoanedIn = log.type == "In (Loan)"
                    )
                    newPlayers.add(p)
                } else {
                    newPlayers.add(Player(
                        name = log.playerName,
                        primaryPosition = "CM",
                        age = 22,
                        startingOverall = 70,
                        overall = 70,
                        potential = 75,
                        valueM = log.feeM,
                        wageK = 10,
                        isLoanedIn = log.type == "In (Loan)",
                        status = "Active"
                    ))
                }
            }
            state.copy(transfers = state.transfers + log, players = newPlayers)
        }
    }
    
    fun deleteTransferLog(logId: String) {
        _state.update { state ->
            val log = state.transfers.find { it.id == logId } ?: return@update state
            val newTransfers = state.transfers.filter { it.id != logId }
            val newPlayers = state.players.toMutableList()
            val existingPlayer = newPlayers.find { it.name == log.playerName || it.displayName == log.playerName }
            
            if (existingPlayer != null) {
                val index = newPlayers.indexOf(existingPlayer)
                when (log.type) {
                    "Out (Permanent)", "Out (Loan)" -> {
                        newPlayers[index] = existingPlayer.copy(status = "Active", isLoanedOut = false)
                    }
                    "In (Permanent)", "In (Loan)", "Free Agent Sign" -> {
                        newPlayers.removeAt(index)
                    }
                }
            }
            state.copy(transfers = newTransfers, players = newPlayers)
        }
    }"""

if old_addTransferLog in content:
    content = content.replace(old_addTransferLog, new_addTransferLog)
    with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
        f.write(content)
    print("Replaced addTransferLog")
else:
    print("Could not find old addTransferLog")

