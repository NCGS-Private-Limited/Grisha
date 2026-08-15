from pathlib import Path


def create_file(path):
    path = Path(path)

    if path.exists():
        return f"{path} already exists"
    else:
        try:
            path.touch()
            return "File Created"
        except FileNotFoundError:
            return "Parent directory does not exist"