from pathlib import Path


def delete_file(path):
    path = Path(path)

    if path.exists():
        if path.is_file():
            try:
                path.unlink()
                return f"File {path} was deleted successfully"
            except OSError:
                return f"File {path} was not deleted successfully"
        else:
            return f"{path} was not a file"
    else:
        return f"{path} does not exist"