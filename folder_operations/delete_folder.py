from pathlib import Path


def folderd(path):
    path = Path(path)

    if path.exists():
        if path.is_dir():
            try:
                path.rmdir()
                return f"Folder {path} was deleted successfully"
            except OSError:
                return f"Folder {path} was not Empty"
        else:
            return f"{path} was not a folder"
    else:
        return f"{path} does not exist"