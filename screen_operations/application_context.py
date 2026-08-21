import win32gui
import win32process

from apps_operations.window_detector import get_visible_windows
from apps_operations.app_database import ApplicationDatabase
from apps_operations.app_matcher import find_best_match
from apps_operations.process_detector import (
    get_running_processes
)

from screen_operations.screen_ocr import (
    detect_text,
    extract_text
)

from screen_operations.element_detector import (
    detect_elements
)


# ============================================================
# FOREGROUND WINDOW
# ============================================================

def get_foreground_window():

    hwnd = win32gui.GetForegroundWindow()

    if not hwnd:
        return None

    if not win32gui.IsWindow(hwnd):
        return None

    title = win32gui.GetWindowText(hwnd)

    try:

        _, pid = (
            win32process.GetWindowThreadProcessId(
                hwnd
            )
        )

    except Exception:
        return None

    return {
        "hwnd": hwnd,
        "pid": pid,
        "title": title
    }


# ============================================================
# FIND PROCESS
# ============================================================

def find_process_by_pid(
    processes,
    pid
):

    for process in processes:

        if process.get("pid") == pid:
            return process

    return None


# ============================================================
# FIND APPLICATION
# ============================================================

def find_application(
    database,
    process
):

    if not process:
        return None

    process_exe = process.get(
        "exe",
        ""
    )

    if not process_exe:
        return None

    process_exe = process_exe.strip().lower()

    # --------------------------------------------------------
    # Search application database
    # --------------------------------------------------------

    for app in database.apps:

        target = app.get(
            "target",
            ""
        )

        if not target:
            continue

        target = target.strip().lower()

        if process_exe == target:
            return app

    return None


# ============================================================
# BUILD APPLICATION CONTEXT
# ============================================================

def get_application_context(
    screenshot=None
):

    # --------------------------------------------------------
    # Foreground window
    # --------------------------------------------------------

    window = get_foreground_window()

    if not window:
        return None

    # --------------------------------------------------------
    # Running processes
    # --------------------------------------------------------

    processes = get_running_processes()

    process = find_process_by_pid(
        processes,
        window["pid"]
    )

    if not process:
        return None

    # --------------------------------------------------------
    # Application database
    # --------------------------------------------------------

    database = ApplicationDatabase()

    application = find_application(
        database,
        process
    )

    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    visible_text = ""
    detected_text = []

    if screenshot is not None:

        visible_text = extract_text(
            screenshot
        )

        detected_text = detect_text(
            screenshot
        )

    # --------------------------------------------------------
    # Screen elements
    # --------------------------------------------------------

    elements = detect_elements()

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    return {
        "application": application,
        "process": process,
        "window": window,
        "visible_text": visible_text,
        "detected_text": detected_text,
        "elements": elements
    }

def get_all_application_context():

    windows = get_visible_windows()

    if not windows:
        return []

    processes = get_running_processes()

    database = ApplicationDatabase()

    foreground_hwnd = win32gui.GetForegroundWindow()

    contexts = []

    for window in windows:

        process = find_process_by_pid(
            processes,
            window["pid"]
        )

        if not process:
            continue

        application = find_application(
            database,
            process
        )

        context = {
            "application": application,
            "process": process,
            "window": window,
            "foreground": (
                    window["hwnd"] == foreground_hwnd
            )
        }

        if not should_include_window(context):
            continue

        contexts.append(context)

    return contexts


# ============================================================
# PRINT CONTEXT
# ============================================================

def print_application_context(
    context
):

    if not context:

        print(
            "Unable to determine application context."
        )

        return

    application = context["application"]
    process = context["process"]
    window = context["window"]

    print()
    print("=" * 60)
    print("APPLICATION CONTEXT")
    print("=" * 60)

    # --------------------------------------------------------
    # Application
    # --------------------------------------------------------

    print()

    print("Application:")

    if application:

        print(
            f"  Name: {application['name']}"
        )

        print(
            f"  Target: {application.get('target', '')}"
        )

    else:

        print("  Unknown")

    # --------------------------------------------------------
    # Process
    # --------------------------------------------------------

    print()

    print("Process:")

    print(
        f"  Name: {process.get('name', '')}"
    )

    print(
        f"  PID: {process.get('pid', '')}"
    )

    print(
        f"  Path: {process.get('path', '')}"
    )

    # --------------------------------------------------------
    # Window
    # --------------------------------------------------------

    print()

    print("Window:")

    print(
        f"  HWND: {window['hwnd']}"
    )

    print(
        f"  Title: {window['title']}"
    )

    print(
        f"  PID: {window['pid']}"
    )

    # --------------------------------------------------------
    # Text
    # --------------------------------------------------------

    print()

    print("Visible text:")

    print(
        context["visible_text"]
    )

    # --------------------------------------------------------
    # Elements
    # --------------------------------------------------------

    print()

    print(
        f"Detected elements: "
        f"{len(context['elements'])}"
    )

    for element in context["elements"]:

        print()

        print(
            f"  Type: "
            f"{element.get('type', '')}"
        )

        print(
            f"  Text: "
            f"{element.get('text', '')}"
        )

        print(
            f"  Position: "
            f"{element.get('center', '')}"
        )

    print()
    print("=" * 60)

def should_include_window(context):

    application = context.get("application")
    window = context.get("window", {})

    title = window.get("title", "").strip()

    # No title
    if not title:
        return False

    # Unknown applications are usually system/background windows
    if not application:
        return False

    app_name = application.get(
        "name",
        ""
    ).strip().lower()

    # --------------------------------------------------------
    # Windows/system applications to ignore
    # --------------------------------------------------------

    ignored_apps = {
        "windows input experience",
        "nvidia geforce overlay",
        "program manager",
        "windows software development kit"
    }

    if app_name in ignored_apps:
        return False

    return True


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from screen_operations.screen_capture import (
        capture_screen
    )

    from screen_operations.screen_processor import (
        process_screen
    )

    print("Capturing screen...")

    screenshot = capture_screen()

    if screenshot is None:

        print("Failed to capture screen.")

    else:

        screenshot = process_screen(
            screenshot
        )

        context = get_application_context(
            screenshot
        )

        print_application_context(
            context
        )