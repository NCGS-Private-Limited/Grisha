import threading

from core.assistant import Assistant
from avatar.overlay import AvatarOverlay
from voice import VoiceEngine
from speech.stt import STTEngine


def main():

    avatar = AvatarOverlay()

    # =================================================
    # VOICE
    # =================================================

    voice = VoiceEngine(
        language="en",
        avatar=avatar
    )

    stt = STTEngine(
        language="en"
    )

    # =================================================
    # ASSISTANT
    # =================================================

    grisha = Assistant(
        avatar,
        voice=voice,
        stt=stt
    )

    # =================================================
    # RUN GRISHA
    # =================================================

    def run_grisha():

        try:

            grisha.start()

        except Exception as e:

            print(
                f"[F1 ERROR] {e}"
            )


        finally:

            voice.close()

            stt.close()

            avatar.root.after(

                0,

                avatar.close

            )

    grisha_thread = threading.Thread(
        target=run_grisha,
        daemon=True
    )

    grisha_thread.start()

    # =================================================
    # TKINTER MAIN LOOP
    # =================================================

    avatar.run()


if __name__ == "__main__":
    main()