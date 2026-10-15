sed -i 's/fun PlayerRowDark(player: Player) {/fun PlayerRowDark(player: Player, onClick: () -> Unit = {}) {/' app/src/main/java/com/example/ui/screens/SquadScreen.kt
