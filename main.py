import threading

from core.assistant import Assistant
from avatar.overlay import AvatarOverlay


def main():

    avatar = AvatarOverlay()
    grisha = Assistant(avatar)

    def run_grisha():

        try:
            grisha.start()

        except Exception as e:
            print(f"[F1 ERROR] {e}")

        finally:
            avatar.root.after(
                0,
                avatar.close
            )

    grisha_thread = threading.Thread(
        target=run_grisha,
        daemon=True
    )

    grisha_thread.start()

    avatar.run()


if __name__ == "__main__":
    main()