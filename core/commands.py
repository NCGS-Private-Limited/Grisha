# General Commands

def hello(name=""):
    if name:
        return f"Hello! {name}"
    return "Hello"

def help():
    return "How can I help?"


def version():
    return "Version F1"

def test_command(first, second, third):
    try:
        return f"{first} {second} {third}"
    except:
        pass