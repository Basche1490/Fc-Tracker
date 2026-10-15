import re, sys

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    # strip comments
    text = re.sub(r'--\[\[.*?\]\]', '', text, flags=re.DOTALL)
    text = re.sub(r'--.*', '', text)
    # strip multiline string literals
    text = re.sub(r'\[\[.*?\]\]', '""', text, flags=re.DOTALL)
    # strip single/double quoted strings
    text = re.sub(r'"(\\.|[^"\\])*"', '""', text)
    text = re.sub(r"'(\\.|[^'\\])*'", "''", text)
    tokens = re.findall(r'\b(?:function|then|do|repeat|until|end)\b', text)
    stack = []
    for t in tokens:
        if t in ('function', 'then', 'do', 'repeat'):
            stack.append(t)
        elif t == 'end':
            if not stack:
                print('Error: unexpected end')
                return False
            opened = stack.pop()
            if opened == 'repeat':
                print('Error: matched repeat with end')
                return False
        elif t == 'until':
            if not stack:
                print('Error: unexpected until')
                return False
            opened = stack.pop()
            if opened != 'repeat':
                print(f'Error: matched {opened} with until')
                return False
    if stack:
        print(f'Error: unclosed {stack}')
        return False
    print(f'{path}: Lua syntax OK! (Tokens: {len(tokens)})')
    return True

if __name__ == '__main__':
    for p in sys.argv[1:]:
        check_file(p)
