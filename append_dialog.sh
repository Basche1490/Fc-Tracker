sed -i '/item { Spacer(Modifier.height(80.dp)) }/!b;n;n;n;a \
\
    editingPlayer?.let {\
        Dialog(onDismissRequest = { editingPlayer = null }) {\
            Box(modifier = Modifier.clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surface).padding(16.dp)) {\
                Column {\
                    Text("Edit Player", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)\
                    Spacer(Modifier.height(8.dp))\
                    Button(onClick = {\
                        onPlayerDelete(it.id)\
                        editingPlayer = null\
                    }, colors = ButtonDefaults.buttonColors(containerColor = Color.Red)) { Text("Delete Player") }\
                    Spacer(Modifier.height(8.dp))\
                    Button(onClick = { editingPlayer = null }) { Text("Close") }\
                }\
            }\
        }\
    }\
' app/src/main/java/com/example/ui/screens/SquadScreen.kt
