from core.commands import hello, test_command
from core.commands import help
from core.commands import version
from core.commands import get_current_time
from file_operations.create_file import create_file
from folder_operations.create_folder import create_folder
from file_operations.delete_file import delete_file
from folder_operations.delete_folder import delete_folder
from file_operations.rename_file import rename_file
from folder_operations.rename_folder import rename_folder
from file_operations.copy_file import copy_file
from folder_operations.copy_folder import copy_folder
from file_operations.move_file import move_file
from folder_operations.move_folder import move_folder
from apps_operations.app_database import ApplicationDatabase
from apps_operations.app_matcher import find_best_match
from apps_operations.app_launcher import open_app
from apps_operations.app_closer import close_application
from apps_operations.window_detector import get_application_windows
from apps_operations.window_matcher import find_best_window
from apps_operations.window_activator import focus_window
from system_operations.system_control import lock_system, hibernate_system
from screen_operations.screen_observer import observe_screen
from actions.elements import click_element
from actions.typing import type_into_element
from actions.selection import SelectionCancelled


commands = {
    "hello": hello,
    "help": help,
    "version": version,
    "test": test_command,
    "time": get_current_time
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
    elif command == "copy":
        if not args:
            return "Copy what?", "failed"
        if args[0] == "file":
            if len(args) == 1:
                return "Enter the file name to copy", "failed"
            elif len(args) == 2:
                return "Enter the destination path to copy the file", "failed"
            elif len(args) == 3:
                result = copy_file(args[1], args[2])
                return result, "Success"
            else:
                return "Invalid Copy command", "failed"
        elif args[0] == "folder":
                if len(args) == 1:
                    return "Enter the folder name to copy", "failed"
                elif len(args) == 2:
                    return "Enter the destination path to copy the folder", "failed"
                elif len(args) == 3:
                    result = copy_folder(args[1], args[2])
                    return result, "Success"
                else:
                    return "Invalid Copy command", "failed"
    elif command == "move":
        if not args:
            return "Move what?", "failed"
        if args[0] == "file":
            if len(args) == 1:
                return "Enter the file name to move", "failed"
            elif len(args) == 2:
                return "Enter the destination path to move the file", "failed"
            elif len(args) == 3:
                result = move_file(args[1], args[2])
                return result, "Success"
            else:
                return "Invalid Move command", "failed"
        elif args[0] == "folder":
            if len(args) == 1:
                return "Enter the folder name to move", "failed"
            elif len(args) == 2:
                return "Enter the destination path to move the folder", "failed"
            elif len(args) == 3:
                result = move_folder(args[1], args[2])
                return result, "Success"
            else:
                return "Invalid Move command", "failed"
        else:
            return "Move what?", "failed"
    elif command == "open":
        if not args:
            return "Enter an application name", "failed"

        application_name = " ".join(args).strip()

        database = ApplicationDatabase()

        app = find_best_match(
            database,
            application_name
        )

        if not app:
            return (
                f"Application not found: {application_name}",
                "failed"
            )

        success, result = open_app(app)

        if success:
            return result, "Success"

        return result, "failed"
    elif command == "close":

        # Validate application name
        if not args:
            return "Enter an application name", "failed"

        application_name = " ".join(args).strip()

        if not application_name:
            return "Enter an application name", "failed"

        # Load application database
        database = ApplicationDatabase()

        # Find the best application match
        app = find_best_match(
            database,
            application_name
        )

        # Application not found
        if not app:
            return (
                f"Application not found: {application_name}",
                "failed"
            )

        # Close application
        result = close_application(app)

        # Application closed successfully
        if result:
            return (
                f"{app['name']} closed.",
                "Success"
            )

        # Application is not running
        return (
            f"{app['name']} is not running.",
            "failed"
        )
    elif command == "focus":

        # --------------------------------------------------------
        # Validate application name
        # --------------------------------------------------------

        if not args:
            return (
                "Enter an application name",
                "failed"
            )

        application_name = " ".join(args).strip()

        if not application_name:
            return (
                "Enter an application name",
                "failed"
            )

        # --------------------------------------------------------
        # Load application database
        # --------------------------------------------------------

        database = ApplicationDatabase()

        # --------------------------------------------------------
        # Find application
        # --------------------------------------------------------

        app = find_best_match(
            database,
            application_name
        )

        if not app:
            return (
                f"Application not found: {application_name}",
                "failed"
            )

        # --------------------------------------------------------
        # Find application windows
        # --------------------------------------------------------

        windows = get_application_windows(app)

        if not windows:
            return (
                f"{app['name']} has no visible windows.",
                "failed"
            )

        # --------------------------------------------------------
        # Select best window
        # --------------------------------------------------------

        window = find_best_window(
            windows
        )

        if not window:
            return (
                f"Could not find a window for {app['name']}.",
                "failed"
            )

        # --------------------------------------------------------
        # Focus window
        # --------------------------------------------------------

        result = focus_window(
            window["hwnd"]
        )

        if result:
            return (
                f"{app['name']} focused.",
                "Success"
            )

        return (
            f"Failed to focus {app['name']}.",
            "failed"
        )
    elif command == "lock":

        if args:
            return (
                "Invalid lock command",
                "failed"
            )

        result = lock_system()

        if result:
            return (
                "System locked.",
                "Success"
            )

        return (
            "Failed to lock system.",
            "failed"
        )
    elif command == "sleep":

        if args:
            return (
                "Invalid sleep command",
                "failed"
            )

        result = hibernate_system()

        if result:
            return (
                "System going to sleep.",
                "Success"
            )

        return (
            "Failed to sleep system.",
            "failed"
        )
    elif command == "observe":

        if args:
            return (
                "Observe does not accept arguments.",
                "failed"
            )

        result, success = observe_screen()

        if success:
            return result, "Success"

        return result, "failed"
    elif command == "click":
        if not args:
            return "Please specify what to click.", "error"

        target = " ".join(args)

        try:
            click_element(target)
            return (
                f'Clicked "{target}".',
                "success"
            )

        except SelectionCancelled:
            return "Cancelled.", "cancelled"

        except ValueError as e:
            return str(e), "error"
    elif command == "type":

        if len(args) < 2:
            return "Please specify an element and text.", "error"

        target = args[0]
        text = " ".join(args[1:])

        try:
            type_into_element(
                target,
                text
            )
            return (
                f'Typed "{text}" into "{target}".',
                "success"
            )
        except SelectionCancelled:
            return "Cancelled.", "cancelled"
        except ValueError as e:
            return str(e), "error"
    else:
        return "Unknown command", "failed"