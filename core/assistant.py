from core.parser import command_split
from core.dispatcher import dispatch
from core.logger import logger
from core.config import config
from apps_operations.app_discovery import discover_and_save_apps


class Assistant:

    def __init__(self, avatar=None):
        self.avatar = avatar

    def _avatar_talking(self):
        if self.avatar:
            self.avatar.root.after(
                0,
                self.avatar.play,
                "talking"
            )

    def _avatar_ideal(self):
        if self.avatar:
            self.avatar.root.after(
                0,
                self.avatar.play,
                "ideal"
            )

    def start(self):

        configuration = config()

        discover_and_save_apps()

        print("Grisha here")

        while True:

            user_input = input("> ")
            user_input = user_input.strip().lower()

            command, args = command_split(
                user_input
            )

            # =============================================
            # EXIT
            # =============================================

            if user_input == "exit":

                logger(
                    user_input,
                    "GoodBye!",
                    "Success"
                )

                break

            # =============================================
            # TALKING
            # =============================================

            self._avatar_talking()

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
            # TEST DELAY
            # =============================================

            self._avatar_ideal()

            # =============================================
            # LOG
            # =============================================

            logger(
                user_input,
                dispatch_output,
                status_output
            )