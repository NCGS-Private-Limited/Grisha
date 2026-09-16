from core.parser import command_split
from core.dispatcher import dispatch
from core.logger import logger
from core.config import config
from apps_operations.app_discovery import discover_and_save_apps


class Assistant:

    def __init__(
        self,
        avatar=None,
        voice=None,
        stt=None,
        wake_word=None
    ):

        self.avatar = avatar
        self.voice = voice
        self.stt = stt
        self.wake_word = wake_word

        self.avatar_mode = False

    # =====================================================
    # AVATAR MODE
    # =====================================================

    def set_avatar_mode(self, enabled):

        self.avatar_mode = enabled

        # ---------------------------------------------
        # STT
        # ---------------------------------------------

        if self.stt:

            if enabled:
                self.stt.stop()
            else:
                self.stt.resume()

        # ---------------------------------------------
        # TTS
        # ---------------------------------------------

        if self.voice:
            self.voice.set_enabled(
                not enabled
            )

    def toggle_avatar_mode(self):

        self.set_avatar_mode(
            not self.avatar_mode
        )

        return self.avatar_mode

    # =====================================================
    # DIALOG
    # =====================================================

    def _show_dialog(self, text):

        if self.avatar and text:

            self.avatar.root.after(
                0,
                self.avatar.show_dialog,
                text
            )

    def _hide_dialog(self):

        if self.avatar:

            self.avatar.root.after(
                0,
                self.avatar.hide_dialog
            )

    # =====================================================
    # RESPONSE
    # =====================================================

    def _respond(self, text):

        if not text:
            return

        # ---------------------------------------------
        # Show dialog
        # ---------------------------------------------

        self._show_dialog(text)

        # ---------------------------------------------
        # Voice
        # ---------------------------------------------

        if self.voice:

            self.voice.speak(text)

        # ---------------------------------------------
        # Hide dialog
        # ---------------------------------------------

        self._hide_dialog()

    # =====================================================
    # START
    # =====================================================

    def start(self):

        configuration = config()

        # ---------------------------------------------
        # Discover applications
        # ---------------------------------------------

        discover_and_save_apps()

        print("Grisha here")

        # =============================================
        # STARTUP GREETING
        # =============================================

        self._respond(
            "Hello, I am Grisha."
        )

        # =============================================
        # MAIN LOOP
        # =============================================

        while True:

            # =========================================
            # STT MODE
            # =========================================

            if self.stt:

                if self.avatar_mode:
                    continue

                wake_detected = (
                    self.stt.wait_for_wake_word()
                )

                if not wake_detected:
                    continue

                if self.avatar_mode:
                    continue

                user_input = self.stt.listen()

            # =========================================
            # KEYBOARD FALLBACK
            # =========================================

            else:

                user_input = input("> ")

                print(user_input)

            # =========================================
            # EMPTY INPUT
            # =========================================

            if not user_input:

                continue

            # =========================================
            # CLEAN INPUT
            # =========================================

            user_input = (
                user_input
                .strip()
                .lower()
            )

            if not user_input:

                continue

            # =========================================
            # WAKE WORD PROCESSING
            # =========================================

            if self.wake_word:

                # -------------------------------------
                # Check wake word
                # -------------------------------------

                if not self.wake_word.is_wake_word(
                    user_input
                ):

                    continue

                # -------------------------------------
                # Remove wake word
                # -------------------------------------

                user_input = (
                    self.wake_word.remove_wake_word(
                        user_input
                    )
                )

                user_input = (
                    user_input
                    .strip()
                    .lower()
                )

                # -------------------------------------
                # Wake word only
                # -------------------------------------

                if not user_input:

                    continue

            # =========================================
            # PARSE COMMAND
            # =========================================

            command, args = command_split(
                user_input
            )

            # =========================================
            # EXIT
            # =========================================

            if user_input in (
                "exit",
                "quit",
                "goodbye",
                "good bye",
                "bye"
            ):

                goodbye = "Goodbye."

                print(
                    f"{configuration['assistant_name']}> "
                    f"{goodbye}"
                )

                logger(
                    user_input,
                    "GoodBye!",
                    "Success"
                )

                # -------------------------------------
                # Goodbye response
                # -------------------------------------

                self._respond(
                    goodbye
                )

                break

            # =========================================
            # EXECUTE COMMAND
            # =========================================

            dispatch_output, status_output = dispatch(
                command,
                args
            )

            # =========================================
            # RESPONSE
            # =========================================

            print(
                f"{configuration['assistant_name']}> "
                f"{dispatch_output}"
            )

            # -----------------------------------------
            # Dialog + Voice
            # -----------------------------------------

            self._respond(
                dispatch_output
            )

            # =========================================
            # LOG
            # =========================================

            logger(
                user_input,
                dispatch_output,
                status_output
            )