cat << 'INNER_EOF' > player_row.kt
@Composable
fun PlayerRowDark(player: Player, onClick: () -> Unit = {}) {
    Box(
        modifier = Modifier
            .clickable { onClick() }
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface)
            .border(1.dp, MaterialTheme.colorScheme.outline, RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.surfaceVariant),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.Person, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "${player.firstName} ${player.lastName}",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onBackground
                )
                Text(
                    text = "${player.primaryPosition} • Age ${player.age} • ${player.morale} • ${player.form}",
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = "€${player.valueM}M • €${player.wageK}K/wk",
                    fontSize = 10.sp,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.Bold
                )
                val tags = mutableListOf<String>()
                if (player.isLoanedOut) tags.add("Out on Loan")
                if (player.isLoanedIn) tags.add("Loaned In")
                if (player.isRegen) tags.add("Regen")
                if (player.isAcademy) tags.add("Academy")
                if (player.isInjured) tags.add("Injured")
                if (tags.isNotEmpty()) {
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.padding(top = 4.dp)) {
                        tags.forEach { tag ->
                            val bgColor = if (tag == "Injured") Color.Red.copy(alpha=0.7f) else MaterialTheme.colorScheme.secondary.copy(alpha = 0.7f)
                            Text(tag, fontSize = 8.sp, color = Color.White, modifier = Modifier.background(bgColor, RoundedCornerShape(4.dp)).padding(horizontal = 4.dp, vertical = 2.dp))
                        }
                    }
                }
            }
            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(8.dp))
                    .background(
                        if (player.overall >= 80) WinColor
                        else if (player.overall >= 70) DrawColor
                        else LossColor
                    )
                    .padding(horizontal = 10.dp, vertical = 4.dp)
            ) {
                Text(
                    text = player.overall.toString(),
                    color = Color(0xFF1A1C18),
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp
                )
            }
        }
    }
}
INNER_EOF
awk -v replace="$(cat player_row.kt)" '
BEGIN { in_func=0 }
/^fun PlayerRowDark/ { in_func=1; print replace; next }
in_func && /^}/ { in_func=0; next }
in_func { next }
{ print }
' app/src/main/java/com/example/ui/screens/SquadScreen.kt > temp_squad.kt
mv temp_squad.kt app/src/main/java/com/example/ui/screens/SquadScreen.kt
