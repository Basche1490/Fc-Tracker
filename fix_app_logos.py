import re
import os

def fix_file(path):
    if not os.path.exists(path): return
    with open(path, "r") as f:
        content = f.read()

    # Replace both 128 and 512 variants of faviconV2
    content = re.sub(
        r'"https://t3\.gstatic\.com/faviconV2\?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://([^&]+)&size=\d+"',
        r'"https://icon.horse/icon/\1"',
        content
    )
    
    with open(path, "w") as f:
        f.write(content)

for root, _, files in os.walk("app/src/main/java/com/example"):
    for f in files:
        if f.endswith(".kt"):
            fix_file(os.path.join(root, f))

