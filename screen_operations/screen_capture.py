from pathlib import Path

from PIL import ImageGrab


SCREENSHOT_DIR = Path("screenshots")


# ============================================================
# CAPTURE ENTIRE SCREEN
# ============================================================

def capture_screen():
    """
    Capture the entire desktop.

    Returns:
        PIL.Image.Image | None
    """

    try:
        screenshot = ImageGrab.grab(
            all_screens=True
        )

        return screenshot

    except Exception:
        return None


# ============================================================
# GET SCREEN RESOLUTION
# ============================================================

def get_screen_resolution():

    try:

        screenshot = capture_screen()

        if screenshot is None:
            return None

        return screenshot.size

    except Exception:
        return None


# ============================================================
# SAVE SCREENSHOT
# ============================================================

def save_screenshot(
    screenshot,
    filename="screen.png"
):

    if screenshot is None:
        return False

    try:

        SCREENSHOT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        path = SCREENSHOT_DIR / filename

        screenshot.save(path)

        return True

    except Exception:
        return False


# ============================================================
# CAPTURE AND SAVE
# ============================================================

def capture_and_save(
    filename="screen.png"
):

    screenshot = capture_screen()

    if screenshot is None:
        return None

    if not save_screenshot(
        screenshot,
        filename
    ):
        return None

    return screenshot


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    screenshot = capture_screen()

    if screenshot is None:

        print("Failed to capture screen.")

    else:

        print(
            f"Screen captured: "
            f"{screenshot.size[0]}x"
            f"{screenshot.size[1]}"
        )

        if save_screenshot(screenshot):

            print(
                "Screenshot saved to "
                "screenshots/screen.png"
            )

        else:

            print("Failed to save screenshot.")