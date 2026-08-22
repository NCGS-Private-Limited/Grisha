import pyautogui
import pytesseract

from PIL import ImageOps, ImageEnhance, ImageFilter


def capture_screen():
    """Capture the entire screen."""
    return pyautogui.screenshot()


def preprocess_images(image):
    """
    Create several versions of the screenshot
    to improve OCR on dark/light UI elements.
    """

    gray = ImageOps.grayscale(image)

    # Upscale
    scaled = gray.resize(
        (gray.width * 2, gray.height * 2)
    )

    # Increase contrast
    contrast = ImageEnhance.Contrast(scaled).enhance(3.0)

    # Sharpen
    sharp = contrast.filter(ImageFilter.SHARPEN)

    # Normal threshold
    binary = sharp.point(
        lambda p: 255 if p > 100 else 0
    )

    # Inverted threshold
    inverted = ImageOps.invert(binary)

    return [
        scaled,
        contrast,
        sharp,
        binary,
        inverted
    ]


def extract_text(image):
    """
    Extract text from the screenshot using
    multiple OCR preprocessing methods.
    """

    images = preprocess_images(image)

    elements = []

    for index, processed in enumerate(images):

        data = pytesseract.image_to_data(
            processed,
            config="--psm 11",
            output_type=pytesseract.Output.DICT
        )

        scale = 2

        for i, text in enumerate(data["text"]):

            text = text.strip()

            if not text:
                continue

            try:
                confidence = float(data["conf"][i])
            except ValueError:
                confidence = -1

            if confidence < 15:
                continue

            # Convert coordinates back to original
            # screenshot coordinates.
            x = data["left"][i] // scale
            y = data["top"][i] // scale
            width = data["width"][i] // scale
            height = data["height"][i] // scale

            elements.append({
                "text": text,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "confidence": confidence,
                "source": index
            })

    return elements


def observe_screen():
    """
    Capture the screen and extract visible text.
    """

    screenshot = capture_screen()

    screenshot.save("screenshots/screen_observation.png")

    elements = extract_text(screenshot)

    return {
        "screenshot": screenshot,
        "elements": elements
    }

def find_element(target):
    """
    Find an element on the screen using OCR.
    """

    screen = observe_screen()

    target = target.strip().lower()

    for element in screen["elements"]:

        detected_text = element["text"].strip().lower()

        if detected_text == target:
            return element

    return None


def get_element_center(element):
    """
    Get the center coordinates of an element.
    """

    x = element["x"]
    y = element["y"]

    width = element["width"]
    height = element["height"]

    center_x = x + width // 2
    center_y = y + height // 2

    return center_x, center_y