import ctypes
import subprocess


def lock_system():

    try:
        result = ctypes.windll.user32.LockWorkStation()

        if result:
            return True

        return False

    except Exception:
        return False


def hibernate_system():

    try:
        result = subprocess.run(
            [
                "shutdown",
                "/h"
            ],
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    except Exception:
        return False


if __name__ == "__main__":

    choice = input(
        "Enter command (lock/sleep): "
    ).strip().lower()

    if choice == "lock":

        if lock_system():
            print("System locked.")
        else:
            print("Failed to lock system.")

    elif choice == "sleep":

        if hibernate_system():
            print("System going to sleep.")
        else:
            print("Failed to sleep system.")

    else:

        print("Unknown command.")