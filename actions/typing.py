from actions.mouse import click
from actions.keyboard import type_text
from actions.screen import find_element, get_element_center


def type_into_element(target, text):
    """
    Find a screen element, click it, and type text.
    """

    element = find_element(target)

    if element is None:
        raise ValueError(
            f'Element "{target}" was not found.'
        )

    x, y = get_element_center(element)

    print(f'Found: {element["text"]}')
    print(f"Clicking field: ({x}, {y})")

    click(x, y)

    print(f"Typing: {text}")

    type_text(text)

    return element