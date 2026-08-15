from core.commands import hello, test_command
from core.commands import help
from core.commands import version
from file_operations.create_file import create_file
from folder_operations.create_folder import create_folder
from file_operations.delete_file import delete_file
from folder_operations.delete_folder import delete_folder
from file_operations.rename_file import rename_file
from folder_operations.rename_folder import rename_folder


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
                    result = create_file(args[1])
                    return result, "Success"

                elif args[0] == "folder":
                    result = create_folder(args[1])
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
                    result = delete_file(args[1])
                    return result, "Success"

                elif args[0] == "folder":
                    result = delete_folder(args[1])
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

    elif command == "rename":
        if not args:
            return "Rename what?", "failed"
        if args[0] == "file":
            if len(args) == 1:
                return "Enter an old file name", "failed"
            elif len(args) == 2:
                return "Enter a new file name", "failed"
            elif len(args) == 3:
                result = rename_file(args[1], args[2])
                return result, "Success"
            else:
                return "Invalid rename command", "failed"
        elif args[0] == "folder":
            if len(args) == 1:
                return "Enter an old folder name", "failed"
            elif len(args) == 2:
                return "Enter a new folder name", "failed"
            elif len(args) == 3:
                result = rename_folder(args[1], args[2])
                return result, "Success"
            else:
                return "Invalid rename command", "failed"
        else:
            return "Rename what?", "failed"

        
    else:
        return "Unknown command", "failed"