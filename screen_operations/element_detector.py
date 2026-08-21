import win32gui

from pywinauto import Desktop


# ============================================================
# CONTROL TYPE MAPPING
# ============================================================

CONTROL_TYPES = {
    "Button": "button",
    "Edit": "text_field",
    "CheckBox": "checkbox",
    "ComboBox": "dropdown",
    "MenuItem": "menu",
    "Menu": "menu",
    "List": "list",
    "ListItem": "list_item",
    "Tab": "tab",
    "Tree": "tree",
    "TreeItem": "tree_item",
    "RadioButton": "radio_button",
    "Slider": "slider",
    "Window": "window",
}


# ============================================================
# GET ELEMENT RECTANGLE
# ============================================================

def get_element_position(element):

    try:

        rect = element.rectangle()

        return {
            "left": rect.left,
            "top": rect.top,
            "right": rect.right,
            "bottom": rect.bottom
        }

    except Exception:
        return None


# ============================================================
# GET ELEMENT CENTER
# ============================================================

def get_element_center(position):

    if not position:
        return None

    x = (
        position["left"]
        + position["right"]
    ) // 2

    y = (
        position["top"]
        + position["bottom"]
    ) // 2

    return {
        "x": x,
        "y": y
    }


# ============================================================
# DETECT WINDOWS
# ============================================================

def detect_application_windows():

    windows = []

    try:

        desktop = Desktop(
            backend="uia"
        )

        for window in desktop.windows():

            try:

                if not window.is_visible():
                    continue

                title = window.window_text()

                position = get_element_position(
                    window
                )

                windows.append({
                    "type": "window",
                    "text": title,
                    "title": title,
                    "position": position,
                    "center": get_element_center(
                        position
                    ),
                    "hwnd": window.handle
                })

            except Exception:
                continue

    except Exception:
        return []

    return windows


# ============================================================
# DETECT UI ELEMENTS
# ============================================================

def detect_elements():

    elements = []

    try:

        desktop = Desktop(
            backend="uia"
        )

        windows = desktop.windows()

        for window in windows:

            try:

                if not window.is_visible():
                    continue

                descendants = window.descendants()

            except Exception:
                continue

            for element in descendants:

                try:

                    if not element.is_visible():
                        continue

                    control_type = (
                        element.element_info.control_type
                    )

                    element_type = CONTROL_TYPES.get(
                        control_type
                    )

                    if not element_type:
                        continue

                    text = element.window_text()

                    position = get_element_position(
                        element
                    )

                    if not position:
                        continue

                    elements.append({
                        "type": element_type,
                        "control_type": control_type,
                        "text": text,
                        "position": position,
                        "center": get_element_center(
                            position
                        ),
                        "hwnd": element.handle
                    })

                except Exception:
                    continue

    except Exception:
        return []

    return elements


# ============================================================
# FILTER ELEMENTS
# ============================================================

def get_elements_by_type(
    elements,
    element_type
):

    return [
        element
        for element in elements
        if element["type"] == element_type
    ]


# ============================================================
# FIND ELEMENT BY TEXT
# ============================================================

def find_element_by_text(
    elements,
    text
):

    query = text.lower().strip()

    matches = []

    for element in elements:

        element_text = (
            element.get("text", "")
            .lower()
            .strip()
        )

        if query in element_text:

            matches.append(element)

    return matches


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("Detecting screen elements...")
    print()

    elements = detect_elements()

    print(
        f"Detected elements: {len(elements)}"
    )

    print()

    for element in elements:

        print(
            f"Type: {element['type']}"
        )

        print(
            f"Text: {element['text']}"
        )

        print(
            f"Position: {element['position']}"
        )

        print(
            f"Center: {element['center']}"
        )

        print(
            f"HWND: {element['hwnd']}"
        )

        print("-" * 60)