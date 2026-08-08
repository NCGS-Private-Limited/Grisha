from core.commands import hello, test_command
from core.commands import help
from core.commands import version


commands = {
    "hello": hello,
    "help": help,
    "version": version,
    "test": test_command
}

def dispatch(command, args):
    if command in commands:
        return commands[command](*args), "Success"
    if command == "exit":
        return "GoodBye!", "Success"
    else:
        return "Unknown command", "failed"