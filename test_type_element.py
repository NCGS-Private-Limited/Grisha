import pyautogui
import pytesseract

from PIL import Image, ImageEnhance, ImageFilter

from actions.typing import type_into_element


def find_text_on_screen(target):
    screenshot = pyautogui.screenshot()

    # Preview area from your current test window.
    # Adjust these if the Preview moves.
    preview = screenshot.crop((850, 150, 1650, 850))

    # Enlarge the image so small UI text is easier for Tesseract to read.
    preview = preview.resize(
        (preview.width * 3, preview.height * 3)
    )

    # Improve contrast.
    gray = preview.convert("L")
    gray = ImageEnhance.Contrast(gray).enhance(2.5)
    gray = gray.filter(ImageFilter.SHARPEN)

    target = target.strip().lower()

    # Try multiple OCR configurations.
    configs = [
        "--psm 6",
        "--psm 11",
        "--psm 12",
    ]

    for config in configs:
        data = pytesseract.image_to_data(
            gray,
            config=config,
            output_type=pytesseract.Output.DICT
        )

        for i, text in enumerate(data["text"]):
            detected_text = text.strip()

            if not detected_text:
                continue

            print(
                f'OCR: "{detected_text}" '
                f'confidence={data["conf"][i]}'
            )

            if detected_text.lower() == target:
                # Coordinates are relative to the cropped image
                x = data["left"][i] // 3 + 850
                y = data["top"][i] // 3 + 150
                width = data["width"][i] // 3
                height = data["height"][i] // 3

                return {
                    "text": detected_text,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                }

    return None


element = find_text_on_screen("Username")

if element:
    print("\n✓ Text detected:")
    print(element)

    type_into_element(
        element,
        "hello world"
    )

    print("✓ Text entered.")

else:
    print('\n✗ "Username" was not detected.')