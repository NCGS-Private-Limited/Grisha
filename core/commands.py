from apps_operations.app_database import ApplicationDatabase
from apps_operations.app_matcher import find_best_match
from apps_operations.app_launcher import open_app

# General Commands

def hello(name=""):
    if name:
        return f"Hello NC"
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

# app commands

def open_command(args):
    if not args:
        return "Application name is required. Usage: open <application>", False

    application_name = " ".join(args).strip()

    database = ApplicationDatabase()

    app = find_best_match(
        database,
        application_name
    )

    if not app:
        return f"Application not found: {application_name}", False

    success, message = open_app(app)

    return message, success