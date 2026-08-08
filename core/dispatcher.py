from core.commands import hello
from core.commands import help
from core.commands import version

commands = {
    "hello": hello,
    "help": help,
    "version": version
}

def dispatch(command, *args):
    if command in commands:
        return commands[command]
    else:
        return "Unknown command"