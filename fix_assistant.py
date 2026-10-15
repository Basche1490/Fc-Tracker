import re

def update_assistant():
    with open("app/src/main/java/com/example/ui/screens/AssistantScreen.kt", "r") as f:
        content = f.read()

    # Find fetchAiResponse
    target_fetch = """suspend fun fetchAiResponse(prompt: String, agent: String, apiUrl: String, apiKey: String): String = withContext(Dispatchers.IO) {
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
        val url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=$geminiKey"
        
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
}"""

    replacement_fetch = """suspend fun fetchAiResponse(prompt: String, agent: String, apiUrl: String, apiKey: String): String = withContext(Dispatchers.IO) {
    if (apiKey.isBlank()) {
        return@withContext "Error: API Key is missing. Please provide it in Settings."
    }

    val client = OkHttpClient.Builder()
        .connectTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
        .readTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
        .build()

    val isGemini = agent.contains("Gemini", ignoreCase = true)

    if (isGemini) {
        val url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=$apiKey"
        
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
            put("model", if (agent.contains("Claude", ignoreCase = true)) "claude-3-haiku-20240307" else if (agent.contains("Grok", ignoreCase = true)) "grok-1" else "gpt-3.5-turbo")
            put("messages", JSONArray().apply {
                put(JSONObject().apply {
                    put("role", "user")
                    put("content", prompt)
                })
            })
            if (agent.contains("Claude", ignoreCase = true)) {
                put("max_tokens", 1024)
            }
        }
        
        val url = if (agent == "Other" && apiUrl.isNotBlank()) {
            if (apiUrl.endsWith("/chat/completions") || apiUrl.endsWith("/messages")) apiUrl else "$apiUrl/chat/completions"
        } else if (agent.contains("ChatGPT", ignoreCase = true)) {
            "https://api.openai.com/v1/chat/completions"
        } else if (agent.contains("Grok", ignoreCase = true)) {
            "https://api.x.ai/v1/chat/completions"
        } else if (agent.contains("Claude", ignoreCase = true)) {
            "https://api.anthropic.com/v1/messages"
        } else {
            "https://api.openai.com/v1/chat/completions"
        }
        
        val requestBuilder = Request.Builder().url(url)
        
        if (agent.contains("Claude", ignoreCase = true)) {
            requestBuilder.addHeader("x-api-key", apiKey)
            requestBuilder.addHeader("anthropic-version", "2023-06-01")
        } else {
            requestBuilder.addHeader("Authorization", "Bearer $apiKey")
        }
        
        val request = requestBuilder
            .post(requestBody.toString().toRequestBody("application/json".toMediaType()))
            .build()
            
        try {
            val response = client.newCall(request).execute()
            if (response.isSuccessful) {
                val responseBody = response.body?.string() ?: ""
                val jsonResponse = JSONObject(responseBody)
                
                if (agent.contains("Claude", ignoreCase = true)) {
                    return@withContext jsonResponse.getJSONArray("content")
                        .getJSONObject(0)
                        .getString("text")
                } else {
                    return@withContext jsonResponse.getJSONArray("choices")
                        .getJSONObject(0)
                        .getJSONObject("message")
                        .getString("content")
                }
            } else {
                return@withContext "Error: ${response.code} ${response.message}"
            }
        } catch (e: Exception) {
            return@withContext "Error: ${e.message}"
        }
    }
}"""
    content = content.replace(target_fetch, replacement_fetch)

    with open("app/src/main/java/com/example/ui/screens/AssistantScreen.kt", "w") as f:
        f.write(content)

update_assistant()
