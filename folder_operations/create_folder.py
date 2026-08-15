from pathlib import Path


def create_folder(path):
    path = Path(path)

    if path.exists():
        return f"{path} already exists"
    else:
        try:
            path.mkdir()
            return "Folder Created"
        except FileNotFoundError:
           return "Parent directory does not exist"