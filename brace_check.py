with open("app/src/main/java/com/example/MainViewModel.kt", "r") as f:
    text = f.read()

depth = 0
in_string = False
in_char = False
escape = False
in_comment = False
in_line_comment = False

for i, c in enumerate(text):
    if in_string:
        if escape: escape = False
        elif c == '\\': escape = True
        elif c == '"': in_string = False
    elif in_char:
        if escape: escape = False
        elif c == '\\': escape = True
        elif c == "'": in_char = False
    elif in_comment:
        if c == '*' and i + 1 < len(text) and text[i+1] == '/':
            in_comment = False
    elif in_line_comment:
        if c == '\n':
            in_line_comment = False
    else:
        if c == '"': in_string = True
        elif c == "'": in_char = True
        elif c == '/' and i + 1 < len(text) and text[i+1] == '*':
            in_comment = True
        elif c == '/' and i + 1 < len(text) and text[i+1] == '/':
            in_line_comment = True
        elif c == '{': depth += 1
        elif c == '}': depth -= 1

print(f"Final depth: {depth}")
