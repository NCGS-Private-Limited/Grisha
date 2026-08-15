from pathlib import Path


def filec(path):
    path = Path(path)

    if path.exists():
        return f"{path} already exists"
    else:
        try:
            path.touch()
            return "File Created"
        except FileNotFoundError:
            return "Parent directory does not exist"