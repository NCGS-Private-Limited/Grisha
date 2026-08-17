from pathlib import Path

def test_file():
    path = Path.cwd()
    print(path)
    print(Path.home)
    file = Path("test.txt")
    print(file.resolve())
    print(file.parent)
