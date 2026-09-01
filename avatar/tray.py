import threading

import pystray
from PIL import Image


class TrayManager:

    def __init__(
        self,
        on_show,
        on_hide,
        on_move,
        on_reset_position,
        on_exit,
    ):
        self.on_show = on_show
        self.on_hide = on_hide
        self.on_move = on_move
        self.on_reset_position = on_reset_position
        self.on_exit = on_exit

        self.icon = None
        self.thread = None

        # Current state
        self.avatar_visible = True
        self.move_enabled = True

    # =====================================================
    # MENU STATE
    # =====================================================

    def _show_checked(self, item):
        return self.avatar_visible

    def _move_checked(self, item):
        return self.move_enabled

    # =====================================================
    # CREATE ICON
    # =====================================================

    def _create_icon(self):

        # Temporary tray icon.
        # Replace with the final Grisha icon later.
        image = Image.new(
            "RGBA",
            (64, 64),
            (30, 30, 30, 255)
        )

        menu = pystray.Menu(

            pystray.MenuItem(
                "Show Avatar",
                self._show,
                checked=self._show_checked
            ),

            pystray.MenuItem(
                "Hide Avatar",
                self._hide
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Move Avatar",
                self._move,
                checked=self._move_checked
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Reset Position",
                self._reset_position
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Exit Grisha",
                self._exit
            ),
        )

        self.icon = pystray.Icon(
            "Grisha",
            image,
            "Grisha",
            menu
        )

    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.icon is not None:
            return

        self._create_icon()

        self.thread = threading.Thread(
            target=self.icon.run,
            daemon=True
        )

        self.thread.start()

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        if self.icon:

            self.icon.stop()

            self.icon = None

    # =====================================================
    # SHOW
    # =====================================================

    def _show(self, icon, item):

        self.avatar_visible = True

        self.on_show()

        icon.update_menu()

    # =====================================================
    # HIDE
    # =====================================================

    def _hide(self, icon, item):

        self.avatar_visible = False

        self.on_hide()

        icon.update_menu()

    # =====================================================
    # MOVE
    # =====================================================

    def _move(self, icon, item):

        self.move_enabled = not self.move_enabled

        self.on_move(
            self.move_enabled
        )

        icon.update_menu()

    # =====================================================
    # RESET POSITION
    # =====================================================

    def _reset_position(self, icon, item):

        self.on_reset_position()

    # =====================================================
    # EXIT
    # =====================================================

    def _exit(self, icon, item):

        self.on_exit()

    # =====================================================
    # EXTERNAL STATE
    # =====================================================

    def set_avatar_visible(self, visible):

        self.avatar_visible = visible

        if self.icon:
            self.icon.update_menu()

    def set_move_enabled(self, enabled):

        self.move_enabled = enabled

        if self.icon:
            self.icon.update_menu()