import re
import sys

def check_lua(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Strip multiline comments --[[ ... ]]
    text = re.sub(r'--\[\[.*?\]\]', '', text, flags=re.DOTALL)
    # Strip single line comments --...
    text = re.sub(r'--.*', '', text)
    # Strip long string literals [[ ... ]]
    text = re.sub(r'\[\[.*?\]\]', '""', text, flags=re.DOTALL)

    # Correct string literal stripping: match both '...' and "..." simultaneously
    text = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '""', text)
    
    # Tokenize Lua keywords
    tokens = re.findall(r'\b(?:function|if|then|elseif|else|while|for|do|repeat|until|end)\b', text)
    stack = []
    
    for t in tokens:
        if t == 'function':
            stack.append('function')
        elif t in ('while', 'for'):
            stack.append('loop_start')
        elif t == 'do':
            if stack and stack[-1] == 'loop_start':
                stack.pop()
                stack.append('do')
            else:
                stack.append('do')
        elif t == 'if':
            stack.append('if')
        elif t == 'then':
            pass
        elif t in ('elseif', 'else'):
            pass
        elif t == 'repeat':
            stack.append('repeat')
        elif t == 'until':
            if not stack or stack[-1] != 'repeat':
                print(f"Error in {filepath}: unexpected until (stack: {stack[-5:]})")
                return False
            stack.pop()
        elif t == 'end':
            if not stack:
                print(f"Error in {filepath}: unexpected end")
                return False
            opened = stack.pop()
            if opened not in ('function', 'do', 'if'):
                print(f"Error in {filepath}: matched {opened} with end")
                return False
                
    if stack:
        print(f"Error in {filepath}: unclosed {stack}")
        return False
    print(f"{filepath}: Syntax balance OK! (Keywords processed: {len(tokens)})")
    return True

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        if not check_lua(arg):
            sys.exit(1)
