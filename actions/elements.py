from actions.mouse import click
from actions.screen import find_element, get_element_center


def click_element(target):
    """
    Find an element on the screen and click it.
    """

    element = find_element(target)

    if element is None:
        raise ValueError(
            f'Element "{target}" was not found.'
        )

    x, y = get_element_center(element)

    print(f'Found: {element["text"]}')
    print(
        f'Bounds: '
        f'({element["x"]}, {element["y"]}) '
        f'{element["width"]}x{element["height"]}'
    )

    print(f"Clicking: ({x}, {y})")

    click(x, y)

    return element