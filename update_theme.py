import re

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'r') as f:
    text = f.read()

replacement = """fun Color.isLight(): Boolean {
    val luminance = 0.299 * this.red + 0.587 * this.green + 0.114 * this.blue
    return luminance > 0.5
}

@Composable
fun FCTheme(
    primaryHex: String = "#bfff00",
    secondaryHex: String = "#ffffff",
    content: @Composable () -> Unit
) {
    val primaryColor = try { Color(android.graphics.Color.parseColor(primaryHex)) } catch (e: Exception) { Color(0xFFBFFF00) }
    val secondaryColor = try { Color(android.graphics.Color.parseColor(secondaryHex)) } catch (e: Exception) { Color.White }
    
    val onPrimaryColor = if (primaryColor.isLight()) Color.Black else Color.White
    val onSecondaryColor = if (secondaryColor.isLight()) Color.Black else Color.White

    val FCColorScheme = darkColorScheme(
        primary = primaryColor,
        secondary = secondaryColor,
        background = Color(0xFF121212),
        surface = Color(0xFF1E1E1E),
        surfaceVariant = Color(0xFF2C2C2C),
        onPrimary = onPrimaryColor,
        onSecondary = onSecondaryColor,
        onBackground = Color.White,
        onSurface = Color.White,
        onSurfaceVariant = Color.LightGray,
        outline = Color(0xFF424242)
    )

    MaterialTheme(
        colorScheme = FCColorScheme,
        typography = Typography,
        content = content
    )
}"""

text = re.sub(r'@Composable\s*fun FCTheme\(.*?\}\s*\}\s*\}', replacement, text, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write(text)

