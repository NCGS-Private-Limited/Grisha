import shutil
from pathlib import Path


def copy_folder(path, des):
    path = Path(path)
    des = Path(des)
    if path.exists():
        if path.is_dir():
            if des.exists():
                return "folder already exists"
            else:
                try:
                    shutil.copytree(path, des)
                    return "folder copied"
                except OSError:
                    return "folder not created"
        else:
            return "Source is not a folder"
    else:
        return "Source does not exist"