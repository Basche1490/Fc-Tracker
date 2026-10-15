sed -i '/var showPlayerForm/a \
    var editingPlayer by remember { mutableStateOf<Player?>(null) }' app/src/main/java/com/example/ui/screens/SquadScreen.kt
sed -i 's/PlayerRowDark(player)/PlayerRowDark(player, onClick = { editingPlayer = player })/' app/src/main/java/com/example/ui/screens/SquadScreen.kt
