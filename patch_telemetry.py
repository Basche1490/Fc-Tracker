import sys
with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    content = f.read()

insert = """
    fun fetchLiveTelemetry() {
        androidx.lifecycle.viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            try {
                // Fetch recent events from ntfy topic (e.g. last 12 hours)
                val url = java.net.URL("https://ntfy.sh/torquay_afc_telemetry_1548/json?since=12h")
                val conn = url.openConnection() as java.net.HttpURLConnection
                conn.requestMethod = "GET"
                val reader = java.io.BufferedReader(java.io.InputStreamReader(conn.inputStream))
                val response = reader.readText()
                reader.close()
                
                val events = mutableListOf<LiveEvent>()
                val lines = response.split("\\n")
                for (line in lines) {
                    if (line.isNotBlank()) {
                        try {
                            val json = org.json.JSONObject(line)
                            if (json.optString("event") == "message") {
                                val title = json.optString("title", "Career Update")
                                val message = json.optString("message", "")
                                val timestamp = json.optLong("time", System.currentTimeMillis() / 1000)
                                events.add(LiveEvent(title, message, timestamp))
                            }
                        } catch (e: Exception) {}
                    }
                }
                _state.update { it.copy(liveEvents = events.sortedByDescending { ev -> ev.timestamp }) }
            } catch (e: Exception) {
                // Ignore connection errors
            }
        }
    }
"""

content = content.replace("fun addNote(title: String, content: String)", insert + "\n    fun addNote(title: String, content: String)")

with open("app/src/main/java/com/example/MainViewModel.kt", "w") as f:
    f.write(content)
