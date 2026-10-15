awk '/^@Composable/ { if(p) print ""; p=1 } /^fun PlayerPitchIcon/ { p=0 } p { print }' app/src/main/java/com/example/ui/screens/FormationTab.kt > temp.kt
cat << 'EOF2' >> temp.kt
@Composable
fun PlayerPitchIcon(player: Player) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        if (player.isInjured) {
            Box(modifier = Modifier.background(Color.Red.copy(alpha=0.8f), RoundedCornerShape(4.dp)).padding(2.dp)) {
                Text("⚠️ Injured", fontSize = 8.sp, color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
        Box(
            modifier = Modifier
                .size(32.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primary),
            contentAlignment = Alignment.Center
        ) {
            if (player.headshotUrl.isNotEmpty()) {
                coil.compose.AsyncImage(
                    model = player.headshotUrl,
                    contentDescription = "Player Face",
                    modifier = Modifier.fillMaxSize(),
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop
                )
            } else {
                Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.onPrimary)
            }
        }
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.background(Color.Black.copy(alpha = 0.6f), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp)) {
            Text(
                "${player.lastName} | ${player.overall}",
                fontSize = 10.sp,
                color = Color.White
            )
        }
        val positions = listOfNotNull(player.primaryPosition, player.secondaryPosition, player.tertiaryPosition).joinToString(", ")
        Text(
            positions,
            fontSize = 8.sp,
            color = Color.LightGray,
            modifier = Modifier.background(Color.Black.copy(alpha = 0.6f), RoundedCornerShape(4.dp)).padding(horizontal = 4.dp)
        )
    }
}
EOF2
mv temp.kt app/src/main/java/com/example/ui/screens/FormationTab.kt
