from pathlib import Path


def rename_folder(old_path, new_path):
    old_path = Path(old_path)
    new_path = Path(new_path)

    if old_path.exists():
        if old_path.is_dir():
            if new_path.exists():
                return "New path already exists"
            else:
                try:
                    old_path.rename(new_path)
                    return "New path was successfully renamed"
                except OSError:
                    return "Path was not renamed"
        else:
            return "Path is not a folder"
    else:
        return f"Folder {old_path} does not exist"