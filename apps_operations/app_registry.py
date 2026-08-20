import re

def create_aliases(app_name):
    name = app_name.lower().strip()

    # Remove special characters
    clean_name = re.sub(r"[^a-z0-9\s]", "", name)

    # Split into words
    words = clean_name.split()

    aliases = set()

    # Original name
    aliases.add(name)

    # Name without spaces
    aliases.add("".join(words))

    # Individual words
    for word in words:
        aliases.add(word)

    # Initials
    if len(words) > 1:
        initials = "".join(word[0] for word in words)
        aliases.add(initials)

    # Special shorthand for Visual Studio Code
    if words == ["visual", "studio", "code"]:
        aliases.add("vscode")
        aliases.add("vs code")

    aliases.discard("")

    return sorted(aliases)