import shutil
from pathlib import Path


def move_file(path, destination):
    path = Path(path)
    destination = Path(destination)

    if path.exists():
        if path.is_file():
            if destination.exists():
                return "File already exists", "failed"
            else:
                try:
                    shutil.move(path, destination)
                    return "File moved successfully", "success"
                except OSError:
                    return "File could not be moved", "failed"
        else:
            return "Move what?", "failed"
    else:
        return "Move what?", "failed"