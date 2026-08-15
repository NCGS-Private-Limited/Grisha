from core.commands import hello, test_command
from core.commands import help
from core.commands import version
from file_operations.create_file import filec
from folder_operations.create_folder import folderc
from file_operations.delete_file import filed
from folder_operations.delete_folder import folderd


commands = {
    "hello": hello,
    "help": help,
    "version": version,
    "test": test_command
}

def dispatch(command, args):
    if command in commands:
        return commands[command](*args), "Success"
    elif command == "exit":
        return "GoodBye!", "Success"
    elif command == "create":
        if not args:
            return "Create what?", "failed"
        else:
            if len(args) > 1:
                if args[0] == "file":
                    result = filec(args[1])
                    return result, "Success"

                elif args[0] == "folder":
                    result = folderc(args[1])
                    return result, "Success"
                else:
                    return "Create what?", "failed"
            else:
                if args[0] == "file":
                    return "Enter a file name", "failed"
                elif args[0] == "folder":
                    return "Enter a folder name", "failed"
                else:
                    return "Create what?", "failed"

    elif command == "delete":
        if not args:
            return "Delete what?", "failed"
        else:
            if len(args) > 1:
                if args[0] == "file":
                    result = filed(args[1])
                    return result, "Success"

                elif args[0] == "folder":
                    result = folderd(args[1])
                    return result, "Success"
                else:
                    return "Delete what?", "failed"
            else:
                if args[0] == "file":
                    return "Enter a file name", "failed"
                elif args[0] == "folder":
                    return "Enter a folder name", "failed"
                else:
                    return "Delete what?", "failed"

    else:
        return "Unknown command", "failed"