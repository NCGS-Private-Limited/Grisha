import threading

from core.assistant import Assistant
from avatar.overlay import AvatarOverlay
from voice import VoiceEngine
from speech.stt import STTEngine
from speech.wake_word import WakeWordEngine
from core.quote_manager import QuoteManager


def main():

    avatar = AvatarOverlay()

    # =================================================
    # VOICE
    # =================================================

    voice = VoiceEngine(
        language="en",
        avatar=avatar
    )

    # =================================================
    # QUOTES
    # =================================================

    quotes = QuoteManager(
        avatar=avatar
    )

    quotes.start()

    stt = STTEngine(
        language="en"
    )

    wake_word = WakeWordEngine()

    # =================================================
    # ASSISTANT
    # =================================================

    grisha = Assistant(
        avatar,
        voice=voice,
        stt=stt,
        wake_word=wake_word
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

            quotes.stop()

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