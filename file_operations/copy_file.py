import shutil
from pathlib import Path


def copy_file(path, des):
    path = Path(path)
    des = Path(des)
    if path.exists():
        if path.is_file():
            if des.exists():
                return "file already exists"
            else:
                try:
                    shutil.copy(path, des)
                    return "file copied"
                except OSError:
                    return "file not created"
        else:
            return "Source is not a file"
    else:
        return "Source does not exist"