import sys
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

new_telemetry_method = """
    private var lastEventId: String = ""

    private fun showLocalNotification(title: String, message: String) {
        val context = getApplication<android.app.Application>()
        val channelId = "ea_fc_telemetry"
        val notificationManager = context.getSystemService(android.content.Context.NOTIFICATION_SERVICE) as android.app.NotificationManager
        
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            val channel = android.app.NotificationChannel(channelId, "Live Updates", android.app.NotificationManager.IMPORTANCE_HIGH)
            notificationManager.createNotificationChannel(channel)
        }
        
        val notification = androidx.core.app.NotificationCompat.Builder(context, channelId)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(title)
            .setContentText(message)
            .setPriority(androidx.core.app.NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()
            
        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }

    fun startTelemetryPolling() {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            while (kotlinx.coroutines.isActive) {
                fetchLiveTelemetry(silent = true)
                kotlinx.coroutines.delay(10000) // Poll every 10 seconds
            }
        }
    }

    fun fetchLiveTelemetry(silent: Boolean = false) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            try {
                val url = java.net.URL("https://ntfy.sh/torquay_afc_telemetry_1548/json?since=1h")
                val conn = url.openConnection() as java.net.HttpURLConnection
                conn.requestMethod = "GET"
                
                val reader = java.io.BufferedReader(java.io.InputStreamReader(conn.inputStream))
                val response = reader.readText()
                reader.close()
                
                val events = _state.value.liveEvents.toMutableList()
                val lines = response.split("\\n")
                
                var newTransfers = _state.value.transfers.toMutableList()
                var newMatches = _state.value.recentMatches.toMutableList()
                var newInjuries = _state.value.activeInjuries
                var hasNew = false
                
                for (line in lines) {
                    if (line.isNotBlank()) {
                        try {
                            val json = org.json.JSONObject(line)
                            val evId = json.optString("id", "")
                            
                            // We only want to process messages that are newer than our last check
                            if (json.optString("event") == "message") {
                                val timestamp = json.optLong("time", System.currentTimeMillis() / 1000)
                                val rawMessage = json.optString("message", "")
                                val rawTitle = json.optString("title", "Career Update")
                                
                                // Check if this is a structured JSON payload disguised as a message string
                                if (rawMessage.startsWith("{") && rawMessage.endsWith("}")) {
                                    val dataObj = org.json.JSONObject(rawMessage)
                                    val dataType = dataObj.optString("dataType")
                                    val evTitle = dataObj.optString("title", rawTitle)
                                    val evMsg = dataObj.optString("message", "")
                                    
                                    // Make sure we haven't processed this exact event yet to avoid duplicates
                                    if (!events.any { it.title == evTitle && it.timestamp == timestamp }) {
                                        events.add(LiveEvent(evTitle, evMsg, timestamp))
                                        hasNew = true
                                        
                                        // Auto-map to AppState based on dataType!
                                        if (dataType == "transfer") {
                                            newTransfers.add(0, TransferLog(
                                                playerName = dataObj.optString("playerName"),
                                                type = dataObj.optString("type"),
                                                feeM = dataObj.optDouble("feeM", 0.0),
                                                fromToClub = dataObj.optString("fromToClub"),
                                                date = dataObj.optString("date")
                                            ))
                                        } else if (dataType == "match") {
                                            newMatches.add(0, MatchResult(
                                                id = "live-${timestamp}",
                                                opponentName = dataObj.optString("opponentName"),
                                                isHome = dataObj.optBoolean("isHome"),
                                                goalsFor = dataObj.optInt("goalsFor"),
                                                goalsAgainst = dataObj.optInt("goalsAgainst"),
                                                resultBadge = dataObj.optString("resultBadge"),
                                                matchDate = dataObj.optString("date"),
                                                competition = dataObj.optString("competition", "League"),
                                                leaguePosition = _state.value.leagueTable.finalRank.toIntOrNull() ?: 1,
                                                opponentCrestUrl = com.example.ui.screens.getTeamCrestUrl(dataObj.optString("opponentName")),
                                                playerPerformances = emptyList()
                                            ))
                                        } else if (dataType == "injury") {
                                            newInjuries += 1
                                        }
                                        
                                        if (silent) {
                                            showLocalNotification(evTitle, evMsg)
                                        }
                                    }
                                } else {
                                    // Standard text message
                                    if (!events.any { it.title == rawTitle && it.timestamp == timestamp }) {
                                        events.add(LiveEvent(rawTitle, rawMessage, timestamp))
                                        hasNew = true
                                        if (silent) {
                                            showLocalNotification(rawTitle, rawMessage)
                                        }
                                    }
                                }
                            }
                        } catch (e: Exception) {}
                    }
                }
                
                if (hasNew) {
                    _state.update { 
                        it.copy(
                            liveEvents = events.sortedByDescending { ev -> ev.timestamp },
                            transfers = newTransfers,
                            recentMatches = newMatches,
                            activeInjuries = newInjuries
                        ) 
                    }
                }
            } catch (e: Exception) {
                // Ignore connection errors
            }
        }
    }
"""

# Replace old fetchLiveTelemetry entirely
import re
# We need to slice out the old fetchLiveTelemetry completely
content = re.sub(r'fun fetchLiveTelemetry\(\) \{.*?(?=fun addNote)', new_telemetry_method, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
