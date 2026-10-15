with open("app/src/main/java/com/example/ui/screens/MatchesScreen.kt", "r") as f:
    content = f.read()
    start = content.find("fun MatchesScreen")
    end = content.find("fun MatchFormModal", start)
    print(content[start:end])
