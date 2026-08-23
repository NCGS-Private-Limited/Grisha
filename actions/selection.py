class SelectionCancelled(Exception):
    """Raised when the user cancels element selection."""
    pass

def select_element(matches):
    """
    Ask the user to select one element.

    Returns:
        dict: Selected element.
        None: If the user cancels.
    """

    while True:

        choice = input("> ").strip()

        # Cancellation
        if choice.lower() in ("cancel", "c"):
            print("Cancelled.")
            return None

        # Non-numeric input
        if not choice.isdigit():
            print("Please enter a number or 'cancel'.")
            continue

        choice = int(choice)

        # Invalid range
        if choice < 1 or choice > len(matches):
            print(
                f"Please enter a number "
                f"between 1 and {len(matches)}, "
                f"or 'cancel'."
            )
            continue

        selected = matches[choice - 1]

        print(
            f'\nSelected: '
            f'{selected["text"]} — '
            f'({selected["x"]}, {selected["y"]})'
        )

        return selected

def resolve_element(target, find_elements):

    matches = find_elements(target)

    if len(matches) == 0:

        raise ValueError(
            f'"{target}" was not found on the screen.'
        )

    if len(matches) == 1:

        return matches[0]

    print(
        f'\nMultiple "{target}" elements found:\n'
    )

    for i, element in enumerate(matches, start=1):

        print(
            f'{i}. '
            f'{element["text"]} — '
            f'({element["x"]}, {element["y"]})'
        )

    print(
        "\nWhich one do you want to use?"
    )

    selected = select_element(matches)

    if selected is None:
        raise SelectionCancelled()

    return selected