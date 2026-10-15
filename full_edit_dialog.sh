cat << 'INNER_EOF' > app/src/main/java/com/example/ui/screens/EditPlayerDialog.kt
package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.Player

@Composable
fun EditPlayerDialog(player: Player, onDismiss: () -> Unit, onUpdate: (Player) -> Unit, onDelete: () -> Unit) {
    var firstName by remember { mutableStateOf(player.firstName) }
    var lastName by remember { mutableStateOf(player.lastName) }
    var overall by remember { mutableStateOf(player.overall.toString()) }
    var isLoanedOut by remember { mutableStateOf(player.isLoanedOut) }
    var isLoanedIn by remember { mutableStateOf(player.isLoanedIn) }
    var isRegen by remember { mutableStateOf(player.isRegen) }
    var isInjured by remember { mutableStateOf(player.isInjured) }
    var isAcademy by remember { mutableStateOf(player.isAcademy) }

    Dialog(onDismissRequest = onDismiss) {
        Box(modifier = Modifier.clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surface).padding(16.dp).heightIn(max = 500.dp)) {
            Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                Text("Edit Player", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(value = firstName, onValueChange = { firstName = it }, label = { Text("First Name") })
                OutlinedTextField(value = lastName, onValueChange = { lastName = it }, label = { Text("Last Name") })
                OutlinedTextField(value = overall, onValueChange = { overall = it }, label = { Text("Overall Rating") })
                
                Row(verticalAlignment = Alignment.CenterVertically) { Checkbox(checked = isLoanedOut, onCheckedChange = { isLoanedOut = it }); Text("Out on Loan", color = Color.White) }
                Row(verticalAlignment = Alignment.CenterVertically) { Checkbox(checked = isLoanedIn, onCheckedChange = { isLoanedIn = it }); Text("Loaned In", color = Color.White) }
                Row(verticalAlignment = Alignment.CenterVertically) { Checkbox(checked = isRegen, onCheckedChange = { isRegen = it }); Text("Regen", color = Color.White) }
                Row(verticalAlignment = Alignment.CenterVertically) { Checkbox(checked = isAcademy, onCheckedChange = { isAcademy = it }); Text("Academy", color = Color.White) }
                Row(verticalAlignment = Alignment.CenterVertically) { Checkbox(checked = isInjured, onCheckedChange = { isInjured = it }); Text("Injured", color = Color.White) }

                Spacer(Modifier.height(16.dp))
                Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                    Button(onClick = onDelete, colors = ButtonDefaults.buttonColors(containerColor = Color.Red)) { Text("Delete") }
                    Button(onClick = {
                        onUpdate(player.copy(
                            firstName = firstName,
                            lastName = lastName,
                            overall = overall.toIntOrNull() ?: player.overall,
                            isLoanedOut = isLoanedOut,
                            isLoanedIn = isLoanedIn,
                            isRegen = isRegen,
                            isAcademy = isAcademy,
                            isInjured = isInjured
                        ))
                        onDismiss()
                    }) { Text("Save") }
                }
            }
        }
    }
}
INNER_EOF
