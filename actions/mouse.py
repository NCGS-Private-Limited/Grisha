import pyautogui


def get_mouse_position():
    """Return the current mouse position as (x, y)."""
    return pyautogui.position()


def move_mouse(x, y):
    """Move the mouse to an absolute screen coordinate."""
    width, height = pyautogui.size()

    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(
            f"Invalid coordinates ({x}, {y}). "
            f"Screen size is {width}x{height}."
        )

    pyautogui.moveTo(x, y)


def move_mouse_relative(dx, dy):
    """Move the mouse relative to its current position."""
    pyautogui.moveRel(dx, dy)


def click(x, y):
    """Move to (x, y) and left-click."""
    move_mouse(x, y)
    pyautogui.click()


def right_click(x, y):
    """Move to (x, y) and right-click."""
    move_mouse(x, y)
    pyautogui.rightClick()


def double_click(x, y):
    """Move to (x, y) and double-click."""
    move_mouse(x, y)
    pyautogui.doubleClick()


def mouse_down(button="left"):
    """Press a mouse button down."""
    pyautogui.mouseDown(button=button)


def mouse_up(button="left"):
    """Release a mouse button."""
    pyautogui.mouseUp(button=button)