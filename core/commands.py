# General Commands

def hello(name=""):
    if name:
        return f"Hello! {name}"
    return "Hello"

def help(topic=""):
    if topic == "hello":
        return "\nhello <name> - Greets a person."
    if topic == "version":
        return "\nversion - version of the Grisha."
    if topic == "/?":
        return ("\nhello : hello <name> - Greets a person.\n"
                "version : version <name> - version of the Grisha.")
    return (
        "\nAvailable commands:\n"
        "hello\n"
        "help\n"
        "version\n"
        "test"
    )


def version():
    return "Version F1"

def test_command(first, second, third):
    try:
        return f"{first} {second} {third}"
    except:
        pass