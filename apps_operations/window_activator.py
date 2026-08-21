import time

import win32api
import win32con
import win32gui
import win32process


def focus_window(hwnd):

    # --------------------------------------------------------
    # Verify HWND
    # --------------------------------------------------------

    if not hwnd:
        return False

    if not win32gui.IsWindow(hwnd):
        return False

    # --------------------------------------------------------
    # Restore minimized window
    # --------------------------------------------------------

    try:

        if win32gui.IsIconic(hwnd):

            win32gui.ShowWindow(
                hwnd,
                win32con.SW_RESTORE
            )

        else:

            win32gui.ShowWindow(
                hwnd,
                win32con.SW_SHOW
            )

    except Exception:
        return False

    # --------------------------------------------------------
    # Get current foreground window
    # --------------------------------------------------------

    try:

        foreground_hwnd = win32gui.GetForegroundWindow()

    except Exception:
        foreground_hwnd = 0

    # --------------------------------------------------------
    # If already focused
    # --------------------------------------------------------

    if foreground_hwnd == hwnd:
        return True

    # --------------------------------------------------------
    # Get thread IDs
    # --------------------------------------------------------

    try:

        current_thread_id = win32api.GetCurrentThreadId()

        target_thread_id, _ = (
            win32process.GetWindowThreadProcessId(hwnd)
        )

        foreground_thread_id, _ = (
            win32process.GetWindowThreadProcessId(
                foreground_hwnd
            )
        ) if foreground_hwnd else (0, 0)

    except Exception:
        return False

    # --------------------------------------------------------
    # Attach input threads when necessary
    # --------------------------------------------------------

    attached_to_target = False
    attached_to_foreground = False

    try:

        if target_thread_id != current_thread_id:

            win32process.AttachThreadInput(
                current_thread_id,
                target_thread_id,
                True
            )

            attached_to_target = True

        if (
            foreground_thread_id
            and foreground_thread_id != current_thread_id
            and foreground_thread_id != target_thread_id
        ):

            win32process.AttachThreadInput(
                current_thread_id,
                foreground_thread_id,
                True
            )

            attached_to_foreground = True

        # ----------------------------------------------------
        # Bring window to top
        # ----------------------------------------------------

        win32gui.BringWindowToTop(hwnd)

        # ----------------------------------------------------
        # Activate window
        # ----------------------------------------------------

        win32gui.SetForegroundWindow(hwnd)

        # ----------------------------------------------------
        # Give Windows a moment
        # ----------------------------------------------------

        time.sleep(0.05)

        # ----------------------------------------------------
        # Verify
        # ----------------------------------------------------

        return win32gui.GetForegroundWindow() == hwnd

    except Exception:

        return False

    finally:

        # ----------------------------------------------------
        # Detach input threads
        # ----------------------------------------------------

        if attached_to_foreground:

            try:

                win32process.AttachThreadInput(
                    current_thread_id,
                    foreground_thread_id,
                    False
                )

            except Exception:
                pass

        if attached_to_target:

            try:

                win32process.AttachThreadInput(
                    current_thread_id,
                    target_thread_id,
                    False
                )

            except Exception:
                pass


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    hwnd = input("Enter HWND: ").strip()

    if not hwnd.isdigit():

        print("Invalid HWND")

    else:

        hwnd = int(hwnd)

        if focus_window(hwnd):

            print("Window focused.")

        else:

            print("Failed to focus window.")