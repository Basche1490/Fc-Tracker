import re

with open("app/src/main/java/com/example/ui/screens/FormationTab.kt", "r") as f:
    lines = f.readlines()

new_lines = []
in_lazy_row = False
brace_count = 0

for line in lines:
    if "LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.padding(8.dp)) {" in line:
        in_lazy_row = True
        brace_count = 1
        new_lines.append(line.replace("LazyRow(horizontalArrangement = Arrangement.spacedBy(16.dp)", "Column(verticalArrangement = Arrangement.spacedBy(16.dp)"))
        continue
        
    if in_lazy_row:
        if "items(players.filter { !it.isStartingXI && !it.isAcademy }) { player ->" in line:
            indent = line[:line.find("items")]
            new_lines.append(indent + "val benchPlayers = players.filter { !it.isStartingXI && !it.isAcademy }\n")
            new_lines.append(indent + "benchPlayers.chunked(6).forEach { rowPlayers ->\n")
            new_lines.append(indent + "    Row(horizontalArrangement = Arrangement.spacedBy(16.dp), modifier = Modifier.fillMaxWidth()) {\n")
            new_lines.append(indent + "        rowPlayers.forEach { player ->\n")
            brace_count += 3
        elif ".width(60.dp)" in line:
            new_lines.append(line.replace(".width(60.dp)", ".weight(1f)"))
        else:
            if "}" in line:
                brace_count -= line.count("}")
                brace_count += line.count("{")
                
                # Check if we are closing the items block
                if brace_count == 1 and line.strip() == "}":
                    indent = line[:line.find("}")]
                    # Wait, if we added 3 braces (chunked, Row, forEach) instead of 1 (items)
                    # we should close 3 braces and add spacers.
                    # This logic is a bit brittle, let's just do it manually with multi_edit_file or python regex.
                    pass
