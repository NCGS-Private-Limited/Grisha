import threading

from core.assistant import Assistant
from avatar.overlay import AvatarOverlay


def main():

    grisha = Assistant()
    avatar = AvatarOverlay()

    def run_grisha():

        try:
            grisha.start()

        except Exception as e:
            print(f"[F1 ERROR] {e}")

        finally:
            # F1 stopped → close F2
            avatar.root.after(
                0,
                avatar.close
            )

    grisha_thread = threading.Thread(
        target=run_grisha,
        daemon=True
    )

    grisha_thread.start()

    # Tkinter must stay on the main thread
    avatar.run()


if __name__ == "__main__":
    main()