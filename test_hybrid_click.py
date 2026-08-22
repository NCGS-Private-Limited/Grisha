from actions.screen import observe_screen
from actions.mouse import click

def main_click(target):
    screen = observe_screen()

    matches = []

    for element in screen["elements"]:

        if element["text"].strip().lower() == target.lower():
            matches.append(element)


    print(f'Found {len(matches)} match(es) for "{target}"')

    for i, element in enumerate(matches):

        print(
            f'\nMatch {i + 1}:'
        )

        print(
            f'  Text: {element["text"]}'
        )

        print(
            f'  Position: '
            f'({element["x"]}, {element["y"]})'
        )

        print(
            f'  Size: '
            f'{element["width"]} x {element["height"]}'
        )

        print(
            f'  Confidence: '
            f'{element["confidence"]:.1f}'
        )


    if not matches:

        print('\n"Save" was not detected.')

    else:

        # For now, click the first match.
        element = matches[0]

        center_x = (
            element["x"] +
            element["width"] // 2
        )

        center_y = (
            element["y"] +
            element["height"] // 2
        )

        print(
            f'\nClicking '
            f'({center_x}, {center_y})'
        )

        click(center_x, center_y)