from actions.screen import find_elements
from actions.selection import select_element


target = "Reload"

print(f'Searching for "{target}"...')

matches = find_elements(target)

print(
    f'\nFound {len(matches)} match(es).\n'
)

if len(matches) == 0:

    print(
        f'"{target}" was not found on the screen.'
    )

elif len(matches) == 1:

    element = matches[0]

    print(
        f'One "{target}" element found.'
    )

    print(
        f'Using: '
        f'({element["x"]}, {element["y"]})'
    )

else:

    print(
        f'Multiple "{target}" elements found:\n'
    )

    for i, element in enumerate(matches, start=1):

        print(
            f'{i}. '
            f'{element["text"]} — '
            f'({element["x"]}, {element["y"]})'
        )

    print(
        '\nWhich one do you want to use?'
    )

    selected = select_element(matches)