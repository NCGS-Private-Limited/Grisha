import re
from difflib import SequenceMatcher

from apps_operations.app_database import ApplicationDatabase


def normalize_name(name):
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9]", "", name)

    return name


def exact_match(apps, query):
    query = query.strip().lower()

    matches = []

    for app in apps:
        if app["name"].lower() == query:
            matches.append(app)

    return matches


def partial_match(apps, query):
    query = query.strip().lower()

    matches = []

    for app in apps:
        app_name = app["name"].lower()

        if query in app_name:
            matches.append(app)

    return matches


def similarity_score(query, name):
    query = normalize_name(query)
    name = normalize_name(name)

    return SequenceMatcher(None, query, name).ratio()


def similar_match(apps, query, threshold=0.60):
    matches = []

    for app in apps:
        score = similarity_score(query, app["name"])

        if score >= threshold:
            matches.append((score, app))

    matches.sort(key=lambda item: item[0], reverse=True)

    return matches


def select_best_duplicate(matches):
    for app in matches:
        target = app.get("target", "")

        if target.lower().endswith(".exe"):
            return app

    return matches[0]


def select_best_partial(matches, query):
    scored = []

    for app in matches:
        score = similarity_score(query, app["name"])
        scored.append((score, app))

    scored.sort(key=lambda item: item[0], reverse=True)

    return scored[0][1]

def alias_match(apps, query):
    query = query.strip().lower()

    matches = []

    for app in apps:
        aliases = app.get("aliases", [])

        for alias in aliases:
            if alias.lower() == query:
                matches.append(app)
                break

    return matches


def find_best_match(database, query):
    apps = database.apps

    # 1. Exact name
    matches = exact_match(apps, query)

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        return select_best_duplicate(matches)

    # 2. Alias
    matches = alias_match(apps, query)

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        return select_best_duplicate(matches)

    # 3. Partial name
    matches = partial_match(apps, query)

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        return select_best_partial(matches, query)

    # 4. Similar name
    matches = similar_match(apps, query)

    if matches:
        return matches[0][1]

    # 5. Nothing found
    return None

if __name__ == "__main__":
    database = ApplicationDatabase()

    tests = [
        "Visual Studio Code",
        "visual studio code",
        "visual",
        "visual studo code",
        "vscode",
        "vs code",
        "code",
        "python",
        "something_that_does_not_exist"
    ]

    for query in tests:
        result = find_best_match(database, query)

        print(f"\nQuery: {query}")

        if result:
            print("Match:", result["name"])
            print("Target:", result["target"])
        else:
            print("No application found.")