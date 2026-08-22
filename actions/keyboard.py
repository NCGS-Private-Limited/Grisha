import pyautogui


def type_text(text):
    """Type the given text."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    pyautogui.write(text)


def press_key(key):
    """Press and release a single key."""
    pyautogui.press(key)


def key_down(key):
    """Press a key and keep it held."""
    pyautogui.keyDown(key)


def key_up(key):
    """Release a held key."""
    pyautogui.keyUp(key)


def hotkey(*keys):
    """Press a key combination."""
    if not keys:
        raise ValueError("At least one key is required")

    pyautogui.hotkey(*keys)