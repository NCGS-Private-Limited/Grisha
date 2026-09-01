import json
from pathlib import Path


class PositionManager:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load(self):
        if not self.file_path.exists():
            return None, 0

        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            position = data.get("avatar_position")

            rotation = int(
                data.get("rotation", 0)
            ) % 360

            if position is None:
                return None, rotation

            return (
                (
                    int(position["x"]),
                    int(position["y"])
                ),
                rotation
            )

        except (OSError, ValueError, TypeError, KeyError):
            return None, 0

    def save(self, x, y, rotation):
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = {
            "avatar_position": {
                "x": int(x),
                "y": int(y)
            },
            "rotation": int(rotation) % 360
        }

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )