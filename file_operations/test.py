from pathlib import Path

def file():
    path = input("Enter the path: ")
    path = Path(path)

    if path.exists():
        print("Path exists")
        if path.is_file():
            print("Is File")
            print(path)
            print(path.name)
            print(path.suffix)
            print(path.parent)
        elif path.is_dir():
            print("Is Directory")
            print(path)
            print(path.name)
            print(path.suffix)
            print(path.parent)
    else:
        print("Path does not exist")