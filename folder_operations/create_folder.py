from pathlib import Path


def folderc(path):
    path = Path(path)

    if path.exists():
        return f"{path} already exists"
    else:
        path.mkdir()
        return "Folder Created"