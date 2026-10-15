with open("app/src/main/java/com/example/ui/screens/MockDesignGalleryScreen.kt", "r") as f:
    text = f.read()

# Fix the broken text strings
text = text.replace('Text("Goals\\nScored"', 'Text("Goals Scored"')
text = text.replace('Text("Goals\nScored"', 'Text("Goals Scored"')
text = text.replace('Text("Clean\\nSheets"', 'Text("Clean Sheets"')
text = text.replace('Text("Clean\nSheets"', 'Text("Clean Sheets"')

with open("app/src/main/java/com/example/ui/screens/MockDesignGalleryScreen.kt", "w") as f:
    f.write(text)
