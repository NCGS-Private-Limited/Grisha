import shutil
from pathlib import Path


def move_folder(path, destination):
    path = Path(path)
    destination = Path(destination)

    if path.exists():
        if path.is_dir():
            if destination.exists():
                return "folder already exists"
            else:
                try:
                    shutil.move(path, destination)
                    return "folder moved successfully"
                except OSError:
                    return "folder does not exist"
        else:
            return "Move what?"
    else:
        return "Move what?"