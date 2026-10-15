import re

with open("app/src/main/java/com/example/ui/screens/AssistantScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports = """import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.MediaType.Companion.toMediaType
import org.json.JSONObject
import org.json.JSONArray
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.coroutines.launch
import com.example.BuildConfig
"""

if "import okhttp3.OkHttpClient" not in content:
    content = content.replace("import androidx.compose.ui.Modifier\n", "import androidx.compose.ui.Modifier\n" + imports)

# We need to inject a coroutine scope
if "val coroutineScope =" not in content:
    content = content.replace("var chatText by remember { mutableStateOf(\"\") }", "var chatText by remember { mutableStateOf(\"\") }\n    val coroutineScope = rememberCoroutineScope()")


fetch_func = """suspend fun fetchAiResponse(prompt: String, agent: String, apiUrl: String, apiKey: String): String = withContext(Dispatchers.IO) {
    val client = OkHttpClient.Builder()
        .connectTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
        .readTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
        .build()

    val useGemini = agent.contains("Free", ignoreCase = true) || apiUrl.isBlank()

    if (useGemini) {
        val geminiKey = BuildConfig.GEMINI_API_KEY
        if (geminiKey.isBlank()) {
            return@withContext "Error: Gemini API Key is missing."
        }
        val url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key=$geminiKey"
        
        val jsonRequest = JSONObject().apply {
            put("contents", JSONArray().apply {
                put(JSONObject().apply {
                    put("parts", JSONArray().apply {
                        put(JSONObject().apply {
                            put("text", prompt)
                        })
                    })
                })
            })
        }
        
        val request = Request.Builder()
            .url(url)
            .post(jsonRequest.toString().toRequestBody("application/json".toMediaType()))
            .build()
            
        try {
            val response = client.newCall(request).execute()
            if (response.isSuccessful) {
                val responseBody = response.body?.string() ?: ""
                val jsonResponse = JSONObject(responseBody)
                return@withContext jsonResponse.getJSONArray("candidates")
                    .getJSONObject(0)
                    .getJSONObject("content")
                    .getJSONArray("parts")
                    .getJSONObject(0)
                    .getString("text")
            } else {
                return@withContext "Error: ${response.code} ${response.message}"
            }
        } catch (e: Exception) {
            return@withContext "Error: ${e.message}"
        }
    } else {
        val requestBody = JSONObject().apply {
            put("model", "gpt-3.5-turbo")
            put("messages", JSONArray().apply {
                put(JSONObject().apply {
                    put("role", "user")
                    put("content", prompt)
                })
            })
        }
        
        val url = if (apiUrl.endsWith("/chat/completions")) apiUrl else "$apiUrl/chat/completions"
        val request = Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer $apiKey")
            .post(requestBody.toString().toRequestBody("application/json".toMediaType()))
            .build()
            
        try {
            val response = client.newCall(request).execute()
            if (response.isSuccessful) {
                val responseBody = response.body?.string() ?: ""
                val jsonResponse = JSONObject(responseBody)
                return@withContext jsonResponse.getJSONArray("choices")
                    .getJSONObject(0)
                    .getJSONObject("message")
                    .getString("content")
            } else {
                return@withContext "Error: ${response.code} ${response.message}"
            }
        } catch (e: Exception) {
            return@withContext "Error: ${e.message}"
        }
    }
}
"""

if "fetchAiResponse" not in content:
    content += "\n" + fetch_func

# Replace the send logic inside keyboardActions and IconButton
send_logic = """if (chatText.isNotBlank()) {
                            val userText = chatText
                            chatHistory = chatHistory + com.example.ui.screens.ChatMessage("user", userText)
                            chatText = ""
                            chatHistory = chatHistory + com.example.ui.screens.ChatMessage("assistant", "Thinking...")
                            coroutineScope.launch {
                                val reply = fetchAiResponse(userText, state.aiAgent, state.aiApiUrl, state.aiApiKey)
                                chatHistory = chatHistory.dropLast(1) + com.example.ui.screens.ChatMessage("assistant", reply)
                            }
                        }"""

old_logic = """if (chatText.isNotBlank()) {
                            chatHistory = chatHistory + com.example.ui.screens.ChatMessage("user", chatText)
                            chatText = ""
                            chatHistory = chatHistory + com.example.ui.screens.ChatMessage("assistant", "I am currently an AI mockup. Once the Gemini API is integrated, I will be able to answer that!")
                        }"""

content = content.replace(old_logic, send_logic)

with open("app/src/main/java/com/example/ui/screens/AssistantScreen.kt", "w") as f:
    f.write(content)
