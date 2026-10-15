import os
import glob
import re

files = glob.glob("app/src/main/java/com/example/ui/screens/*.kt")

for file in files:
    with open(file, "r") as f:
        content = f.read()

    new_content = content.replace("https://logo.clearbit.com/", "https://icon.horse/icon/")
    # Wait, logo.clearbit.com/$domain?size=256 -> icon.horse/icon/$domain?size=256
    # icon.horse doesn't use ?size=256 in the same way (it might ignore it), but it's fine.
    # Actually let's just replace https://logo.clearbit.com with https://icon.horse/icon
    
    if new_content != content:
        with open(file, "w") as f:
            f.write(new_content)
        print(f"Updated {file}")

