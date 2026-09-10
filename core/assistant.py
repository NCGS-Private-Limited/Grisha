from core.parser import command_split
from core.dispatcher import dispatch
from core.logger import logger
from core.config import config
from apps_operations.app_discovery import discover_and_save_apps


class Assistant:

    def __init__(self, avatar=None, voice=None, stt=None):

        self.avatar = avatar
        self.voice = voice
        self.stt = stt

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

        # Dialog appears
        self._show_dialog(text)

        # Voice + talking animation
        if self.voice:
            self.voice.speak(text)

        # Voice/action finished → dialog disappears
        self._hide_dialog()

    # =====================================================
    # START
    # =====================================================

    def start(self):

        configuration = config()

        discover_and_save_apps()

        print("Grisha here")

        # =============================================
        # STARTUP GREETING
        # =============================================

        self._respond(
            "Hello, I am Grisha."
        )

        while True:

            if self.stt:

                user_input = self.stt.listen()

            else:

                user_input = input("> ")

            user_input = (
                user_input
                .strip()
                .lower()
            )

            # =============================================
            # EMPTY INPUT
            # =============================================

            if not user_input:
                continue

            command, args = command_split(
                user_input
            )

            # =============================================
            # EXIT
            # =============================================

            if user_input in (
                "exit",
                "quit",
                "goodbye",
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

                # -----------------------------------------
                # Show Goodbye dialog + voice
                # -----------------------------------------

                self._respond(
                    goodbye
                )

                # -----------------------------------------
                # Hide dialog after voice
                # -----------------------------------------

                self._hide_dialog()

                break

            # =============================================
            # EXECUTE COMMAND
            # =============================================

            dispatch_output, status_output = dispatch(
                command,
                args
            )

            # =============================================
            # RESPONSE
            # =============================================

            print(
                f"{configuration['assistant_name']}> "
                f"{dispatch_output}"
            )

            # =============================================
            # DIALOG + VOICE
            # =============================================

            self._respond(
                dispatch_output
            )

            # =============================================
            # LOG
            # =============================================

            logger(
                user_input,
                dispatch_output,
                status_output
            )