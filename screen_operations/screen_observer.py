from screen_operations.screen_capture import capture_screen
from screen_operations.screen_processor import process_screen
from screen_operations.application_context import (
    get_application_context,
    get_all_application_context
)
from screen_operations.screen_understanding import (
    understand_screen,
    describe_screen
)



def observe_screen():

    screenshot = capture_screen()

    if screenshot is None:
        return (
            "Failed to capture the screen.",
            False
        )

    screenshot = process_screen(
        screenshot
    )

    if screenshot is None:
        return (
            "Failed to process the screen.",
            False
        )

    # --------------------------------------------------------
    # Foreground application context
    # --------------------------------------------------------

    context = get_application_context(
        screenshot
    )

    if context is None:
        return (
            "Unable to determine screen context.",
            False
        )

    # --------------------------------------------------------
    # All visible windows
    # --------------------------------------------------------

    all_windows = get_all_application_context()

    # --------------------------------------------------------
    # Understand
    # --------------------------------------------------------

    understanding = understand_screen(
        context,
        all_windows
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    response = describe_screen(
        understanding
    )

    return response, True