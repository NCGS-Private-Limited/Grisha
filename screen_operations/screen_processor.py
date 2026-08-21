from PIL import Image


# ============================================================
# RESIZE IMAGE
# ============================================================

def resize_image(
    image,
    max_width=1920,
    max_height=1080
):
    """
    Resize an image while preserving its aspect ratio.

    Returns:
        PIL.Image.Image
    """

    if image is None:
        return None

    width, height = image.size

    # No resizing required
    if width <= max_width and height <= max_height:
        return image.copy()

    # Create a copy so the original is not modified
    processed = image.copy()

    processed.thumbnail(
        (max_width, max_height),
        Image.Resampling.LANCZOS
    )

    return processed


# ============================================================
# CONVERT IMAGE
# ============================================================

def prepare_image(image):

    if image is None:
        return None

    # Convert to RGB for consistent OCR/vision input
    if image.mode != "RGB":
        image = image.convert("RGB")

    return image


# ============================================================
# PROCESS SCREEN
# ============================================================

def process_screen(
    image,
    max_width=1920,
    max_height=1080
):
    """
    Prepare a captured screen image for analysis.

    Pipeline:

        Capture
          ↓
        RGB
          ↓
        Resize
          ↓
        Analysis-ready image
    """

    if image is None:
        return None

    # --------------------------------------------------------
    # Convert
    # --------------------------------------------------------

    processed = prepare_image(image)

    # --------------------------------------------------------
    # Resize
    # --------------------------------------------------------

    processed = resize_image(
        processed,
        max_width,
        max_height
    )

    return processed


# ============================================================
# GET IMAGE INFORMATION
# ============================================================

def get_image_info(image):

    if image is None:
        return None

    return {
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "format": image.format
    }


# ============================================================
# SAVE PROCESSED IMAGE
# ============================================================

def save_processed_image(
    image,
    path="screenshots/processed_screen.png"
):

    if image is None:
        return False

    try:

        image.save(
            path,
            format="PNG"
        )

        return True

    except Exception:
        return False


# ============================================================
# TEST
# ============================================================
def test12():
        from screen_operations.screen_capture import (
            capture_screen
        )

        print("Capturing screen...")

        screenshot = capture_screen()

        if screenshot is None:

            print("Failed to capture screen.")

        else:

            print(
                f"Original: "
                f"{screenshot.width}x"
                f"{screenshot.height}"
            )

            processed = process_screen(
                screenshot
            )

            if processed is None:

                print("Failed to process screen.")

            else:

                print(
                    f"Processed: "
                    f"{processed.width}x"
                    f"{processed.height}"
                )

                print(
                    f"Mode: "
                    f"{processed.mode}"
                )

                if save_processed_image(
                    processed
                ):

                    print(
                        "Saved: "
                        "screenshots/processed_screen.png"
                    )

                else:

                    print(
                        "Failed to save processed image."
                    )