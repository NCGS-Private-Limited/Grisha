import psutil
import win32gui
import win32con

from apps_operations.process_detector import find_application_processes
from apps_operations.window_detector import get_application_windows



def close_window(hwnd):

    if not win32gui.IsWindow(hwnd):
        return False

    win32gui.PostMessage(
        hwnd,
        win32con.WM_CLOSE,
        0,
        0
    )

    return True


def close_process(pid):

    try:

        process = psutil.Process(pid)

        process.terminate()

        return True

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied
    ):

        return False


def close_application_window(window):

    hwnd = window.get("hwnd")

    if not hwnd:
        return False

    return close_window(hwnd)


def close_application(app):

    windows = get_application_windows(app)

    if not windows:
        return False

    closed = 0

    for window in windows:

        if close_application_window(window):
            closed += 1

    return closed > 0