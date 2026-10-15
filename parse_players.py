import re

with open('app/src/main/java/com/example/MainViewModel.kt', 'r') as f:
    text = f.read()

# Add application parameter
text = text.replace('class MainViewModel : ViewModel() {', 'class MainViewModel(application: android.app.Application) : androidx.lifecycle.AndroidViewModel(application) {')

data_class = """
data class EafcPlayer(
    val id: String,
    val name: String,
    val commonName: String,
    val birthdate: String,
    val position: String,
    val alternatePositions: String,
    val nationality: String,
    val team: String,
    val overallRating: Int
)
"""
if 'data class EafcPlayer' not in text:
    text = text.replace('data class Player(', data_class + '\ndata class Player(')

text = text.replace('    val overall: Int,', '    val startingOverall: Int = 0,\n    val overall: Int,')

with open('app/src/main/java/com/example/MainViewModel.kt', 'w') as f:
    f.write(text)
