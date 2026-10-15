with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "r") as f:
    content = f.read()

old_call = "1 -> FormationTab(activeSquad, Modifier.weight(1f), onPlayerUpdate = { viewModel.updatePlayer(it) }, onApplyFormation = { viewModel.updatePlayers(it) })"
new_call = "1 -> FormationTab(activeSquad, Modifier.weight(1f), onPlayerUpdate = { viewModel.updatePlayer(it) }, onApplyFormation = { viewModel.updatePlayers(it) }, onSwapPlayers = { id1, id2 -> viewModel.swapPlayers(id1, id2) })"
content = content.replace(old_call, new_call)

with open("app/src/main/java/com/example/ui/screens/SquadScreen.kt", "w") as f:
    f.write(content)

