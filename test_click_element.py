import pyautogui
import pytesseract

from actions.mouse import click


def find_text_on_screen(target):
    """
    Find text on the current screen using Tesseract OCR.

    Returns:
        {
            "text": "...",
            "x": ...,
            "y": ...,
            "width": ...,
            "height": ...
        }

    or None if the text is not found.
    """

    screenshot = pyautogui.screenshot()

    data = pytesseract.image_to_data(
        screenshot,
        output_type=pytesseract.Output.DICT
    )

    target = target.strip().lower()

    for i, text in enumerate(data["text"]):
        detected_text = text.strip()

        if not detected_text:
            continue

        if detected_text.lower() == target:
            x = data["left"][i]
            y = data["top"][i]
            width = data["width"][i]
            height = data["height"][i]

            return {
                "text": detected_text,
                "x": x,
                "y": y,
                "width": width,
                "height": height
            }

    return None


def click_detected_element(target):
    print(f'Searching for "{target}"...')

    element = find_text_on_screen(target)

    if element is None:
        print(f'✗ Could not find "{target}" on screen.')
        return False

    print("Detected:")
    print(f'  Text: {element["text"]}')
    print(f'  Position: ({element["x"]}, {element["y"]})')
    print(f'  Size: {element["width"]} x {element["height"]}')

    center_x = element["x"] + element["width"] // 2
    center_y = element["y"] + element["height"] // 2

    print(f"  Click position: ({center_x}, {center_y})")

    click(center_x, center_y)

    print("✓ Clicked.")

    return True


if __name__ == "__main__":
    click_detected_element("Reload")