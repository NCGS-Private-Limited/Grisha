from actions.screen import find_elements
from actions.selection import resolve_element
from actions.mouse import click


def click_element(target):

    element = resolve_element(
        target,
        find_elements
    )

    center_x = (
        element["x"] +
        element["width"] // 2
    )

    center_y = (
        element["y"] +
        element["height"] // 2
    )

    print(
        f'Clicking "{element["text"]}" '
        f'at ({center_x}, {center_y})'
    )

    click(center_x, center_y)

    return element