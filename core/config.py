import json
from pathlib import Path

def config():
    config_file = Path("config/settings.json")

    default_settings = {
        "assistant_name": "Grisha",
        "theme": "dark"
    }

    if config_file.exists():
        with config_file.open("r") as file:
            settings = json.load(file)
            return settings
    else:
        with config_file.open("w") as file:
            json.dump(default_settings, file)
            return default_settings