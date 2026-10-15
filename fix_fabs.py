import re
import os
import glob

for filepath in glob.glob("app/src/main/java/com/example/ui/screens/*.kt"):
    with open(filepath, "r") as f:
        content = f.read()
    
    # Replace multiline modifier for FABs
    content = content.replace(".align(Alignment.BottomEnd)\n                .padding(16.dp)", ".align(Alignment.BottomEnd)\n                .navigationBarsPadding()\n                .padding(16.dp)")
    content = content.replace(".align(Alignment.BottomEnd)\n            .padding(16.dp)", ".align(Alignment.BottomEnd)\n            .navigationBarsPadding()\n            .padding(16.dp)")
    content = content.replace("Modifier.align(Alignment.BottomEnd).padding(16.dp)", "Modifier.align(Alignment.BottomEnd).navigationBarsPadding().padding(16.dp)")

    with open(filepath, "w") as f:
        f.write(content)

