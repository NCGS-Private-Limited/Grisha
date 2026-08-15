from core.commands import hello, test_command
from core.commands import help
from core.commands import version
from file_operations.create_file import filec
from folder_operations.create_folder import folderc


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
    if command == "create" and args[0] == "file":
        filec(args[1])
    if command == "create" and args[0] == "folder":
        folderc(args[1])
    else:
        return "Unknown command1", "failed"