import pytesseract

from pytesseract import Output


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

# If Tesseract is not in PATH, uncomment and change this:
#
# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


# ============================================================
# DETECT TEXT
# ============================================================

def detect_text(image):

    if image is None:
        return []

    try:

        data = pytesseract.image_to_data(
            image,
            output_type=Output.DICT
        )

    except Exception:
        return []

    results = []

    total_items = len(data["text"])

    for index in range(total_items):

        text = data["text"][index].strip()

        if not text:
            continue

        try:

            confidence = float(
                data["conf"][index]
            )

        except (ValueError, TypeError):
            confidence = -1

        x = data["left"][index]
        y = data["top"][index]
        width = data["width"][index]
        height = data["height"][index]

        results.append({
            "text": text,
            "confidence": confidence,
            "position": {
                "x": x,
                "y": y
            },
            "size": {
                "width": width,
                "height": height
            },
            "box": {
                "left": x,
                "top": y,
                "right": x + width,
                "bottom": y + height
            }
        })

    return results


# ============================================================
# EXTRACT TEXT ONLY
# ============================================================

def extract_text(image):

    if image is None:
        return ""

    try:

        return pytesseract.image_to_string(
            image
        ).strip()

    except Exception:
        return ""


# ============================================================
# GROUP DETECTED WORDS
# ============================================================

def get_text_regions(image):

    if image is None:
        return []

    try:

        data = pytesseract.image_to_data(
            image,
            output_type=Output.DICT
        )

    except Exception:
        return []

    regions = []

    total_items = len(data["text"])

    current_region = None

    for index in range(total_items):

        text = data["text"][index].strip()

        if not text:
            continue

        try:
            confidence = float(
                data["conf"][index]
            )
        except (ValueError, TypeError):
            confidence = -1

        x = data["left"][index]
        y = data["top"][index]
        width = data["width"][index]
        height = data["height"][index]

        block = data["block_num"][index]
        paragraph = data["par_num"][index]

        # ----------------------------------------------------
        # Start a new region
        # ----------------------------------------------------

        region_id = (
            block,
            paragraph
        )

        if (
            current_region is None
            or current_region["id"] != region_id
        ):

            if current_region is not None:
                regions.append(
                    current_region
                )

            current_region = {
                "id": region_id,
                "text": text,
                "confidence": confidence,
                "box": {
                    "left": x,
                    "top": y,
                    "right": x + width,
                    "bottom": y + height
                }
            }

        else:

            # ------------------------------------------------
            # Add word to existing region
            # ------------------------------------------------

            current_region["text"] += " " + text

            current_region["confidence"] = (
                current_region["confidence"]
                + confidence
            ) / 2

            current_region["box"]["left"] = min(
                current_region["box"]["left"],
                x
            )

            current_region["box"]["top"] = min(
                current_region["box"]["top"],
                y
            )

            current_region["box"]["right"] = max(
                current_region["box"]["right"],
                x + width
            )

            current_region["box"]["bottom"] = max(
                current_region["box"]["bottom"],
                y + height
            )

    if current_region is not None:
        regions.append(current_region)

    return regions


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

        print("Processing screen...")

        image = process_screen(
            screenshot
        )

        print()
        print("Detected text:")
        print("-" * 60)

        text = extract_text(image)

        print(text)

        print()
        print("Detected text positions:")
        print("-" * 60)

        detected = detect_text(image)

        for item in detected:

            print(
                f"{item['text']} "
                f"-> "
                f"({item['position']['x']}, "
                f"{item['position']['y']}) "
                f"confidence="
                f"{item['confidence']:.1f}"
            )