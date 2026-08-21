import win32gui
import win32process
from apps_operations.process_detector import find_application_processes

def get_visible_windows():

    windows = []

    def callback(hwnd, extra):

        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)

        if not title:
            return

        try:

            _, pid = win32process.GetWindowThreadProcessId(
                hwnd
            )

        except Exception:
            return

        windows.append({
            "hwnd": hwnd,
            "title": title,
            "pid": pid
        })

    win32gui.EnumWindows(
        callback,
        None
    )

    return windows

def get_application_windows(app):

    processes = find_application_processes(app)

    if not processes:
        return []

    process_ids = {
        process["pid"]
        for process in processes
    }

    windows = get_visible_windows()

    application_windows = []

    for window in windows:

        if window["pid"] in process_ids:

            application_windows.append(window)

    return application_windows