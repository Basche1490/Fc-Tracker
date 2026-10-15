import re

with open("app/build.gradle.kts", "r") as f:
    content = f.read()

if "com.google.code.gson:gson" not in content:
    content = content.replace("dependencies {", "dependencies {\n    implementation(\"com.google.code.gson:gson:2.10.1\")")
    with open("app/build.gradle.kts", "w") as f:
        f.write(content)
