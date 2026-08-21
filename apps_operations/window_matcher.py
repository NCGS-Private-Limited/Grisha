from difflib import SequenceMatcher


def normalize(text):
    return (
        text
        .lower()
        .strip()
    )


def calculate_similarity(query, title):

    query = normalize(query)
    title = normalize(title)

    if not query or not title:
        return 0

    # Exact title
    if query == title:
        return 100

    # Query appears directly in title
    if query in title:
        return 90

    # Compare similarity
    return int(
        SequenceMatcher(
            None,
            query,
            title
        ).ratio() * 100
    )


def find_best_window(windows, query=None):

    if not windows:
        return None

    # No specific window requested.
    # Use the first available window.
    if not query:

        return windows[0]

    query = normalize(query)

    best_window = None
    best_score = 0

    for window in windows:

        title = window.get(
            "title",
            ""
        )

        score = calculate_similarity(
            query,
            title
        )

        if score > best_score:

            best_score = score
            best_window = window

    return best_window