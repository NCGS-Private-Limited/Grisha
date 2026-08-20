from pathlib import Path
import json


APPS_FILE = Path("config/apps.json")


class ApplicationDatabase:

    def __init__(self):
        self.apps = []
        self.load()

    def load(self):
        if not APPS_FILE.exists():
            self.apps = []
            return False

        try:
            with open(APPS_FILE, "r", encoding="utf-8") as file:
                self.apps = json.load(file)

            return True

        except (json.JSONDecodeError, OSError):
            self.apps = []
            return False

    def find(self, name):
        name = name.strip().lower()

        for app in self.apps:
            if app["name"].lower() == name:
                return app

        return None

    def find_all(self, name):
        name = name.strip().lower()

        results = []

        for app in self.apps:
            if app["name"].lower() == name:
                results.append(app)

        return results

    def search(self, query):
        query = query.strip().lower()

        results = []

        for app in self.apps:
            if query in app["name"].lower():
                results.append(app)

        return results

    def refresh(self):
        return self.load()