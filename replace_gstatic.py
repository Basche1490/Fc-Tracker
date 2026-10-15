import os
import glob
import re

files = glob.glob("app/src/main/java/com/example/ui/screens/*.kt")

for file in files:
    with open(file, "r") as f:
        content = f.read()

    new_content = content.replace(
        '"https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${domain}&size=256"',
        '"https://logo.clearbit.com/${domain}?size=256"'
    )
    
    new_content = new_content.replace(
        '"https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://${exactMatch.value}&size=256"',
        '"https://logo.clearbit.com/${exactMatch.value}?size=256"'
    )
    
    new_content = new_content.replace(
        '"https://t3.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://$domain&size=256"',
        '"https://logo.clearbit.com/$domain?size=256"'
    )

    if new_content != content:
        with open(file, "w") as f:
            f.write(new_content)
        print(f"Updated {file}")

