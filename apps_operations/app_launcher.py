import subprocess
import shlex
from pathlib import Path


def open_app(app):
    if not app:
        return False, "Application was not found."

    # Get executable
    target = app.get("target")

    if not target:
        return False, "Application target is missing."

    target_path = Path(target)

    if not target_path.exists():
        return False, f"Application executable not found: {target}"

    if not target_path.is_file():
        return False, f"Application target is not a file: {target}"

    # Get arguments
    arguments = app.get("arguments", "")

    if arguments:
        try:
            args = shlex.split(arguments, posix=False)
        except ValueError as error:
            return False, f"Invalid application arguments: {error}"
    else:
        args = []

    # Build command
    command = [str(target_path)] + args

    # Get working directory
    working_directory = app.get("working_directory")
    cwd = None

    if working_directory:
        working_directory_path = Path(working_directory)

        if working_directory_path.exists() and working_directory_path.is_dir():
            cwd = str(working_directory_path)

    # Launch application
    try:
        subprocess.Popen(
            command,
            cwd=cwd
        )

    except FileNotFoundError:
        return False, "Application executable could not be found."

    except PermissionError:
        return False, "Permission denied while launching the application."

    except OSError as error:
        return False, f"Failed to launch application: {error}"

    return True, f"Opened {app['name']}."

if __name__ == "__main__":
    from app_database import ApplicationDatabase
    from app_matcher import find_best_match

    database = ApplicationDatabase()

    app = find_best_match(database, "file explorer")

    if app:
        success, message = open_app(app)
        print(message)
        print("Status:", success)
    else:
        print("Application not found.")