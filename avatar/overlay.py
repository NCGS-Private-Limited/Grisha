from pathlib import Path
import ctypes
import tkinter as tk

from .renderer import AvatarRenderer
from .player import AvatarPlayer
from .position import PositionManager
from .context_menu import AvatarContextMenu
from .tray import TrayManager


class AvatarOverlay:

    GWL_EXSTYLE = -20

    WS_EX_TRANSPARENT = 0x00000020
    WS_EX_TOOLWINDOW = 0x00000080
    WS_EX_NOACTIVATE = 0x08000000

    SM_XVIRTUALSCREEN = 76
    SM_YVIRTUALSCREEN = 77
    SM_CXVIRTUALSCREEN = 78
    SM_CYVIRTUALSCREEN = 79

    ROTATIONS = (
        0,
        90,
        180,
        270
    )

    def __init__(
        self,
        base_dir=None
    ):

        # =================================================
        # PATHS
        # =================================================

        self.base_dir = (
            Path(base_dir)
            if base_dir
            else Path(__file__).parent
        )

        self.animations_dir = (
            self.base_dir
            / "animations"
        )

        self.position_file = (
            self.base_dir
            / "position.json"
        )

        # =================================================
        # TKINTER
        # =================================================

        self.root = tk.Tk()

        self.root.overrideredirect(True)

        self.root.attributes(
            "-topmost",
            True
        )

        self.root.attributes(
            "-toolwindow",
            True
        )

        # Transparent background
        self.transparent_color = "#010101"

        self.root.configure(
            bg=self.transparent_color
        )

        self.root.attributes(
            "-transparentcolor",
            self.transparent_color
        )

        # =================================================
        # STATE
        # =================================================

        self.animation = "ideal"
        self.rotation = 0

        self.x = 0
        self.y = 0

        self.avatar_width = 0
        self.avatar_height = 0

        # Move Avatar is ENABLED at startup
        self.move_mode = True

        # Therefore click-through starts disabled
        self.click_through = False

        self.dragging = False

        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Tray
        self.tray = None

        # Windows handle
        self.hwnd = None

        # =================================================
        # RENDERER
        # =================================================

        self.renderer = AvatarRenderer(
            self.animations_dir,
            scale=0.25
        )

        # =================================================
        # POSITION
        # =================================================

        self.position_manager = (
            PositionManager(
                self.position_file
            )
        )

        # =================================================
        # AVATAR LABEL
        # =================================================

        self.label = tk.Label(
            self.root,
            bg=self.transparent_color,
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )

        self.label.pack()

        # =================================================
        # PLAYER
        # =================================================

        self.player = AvatarPlayer(
            self.root,
            self.renderer,
            self.show_frame,
            fps=24,
            ideal_speed=1.5,
            talking_speed=1.15,
            ideal_hold=2.0
        )

        # =================================================
        # CONTEXT MENU
        # =================================================

        self.context_menu = (
            AvatarContextMenu(
                self.root,

                on_move=self.set_move_mode,

                on_click_through_toggle=(
                    self.set_click_through
                ),

                on_rotation=self.set_rotation,

                on_reset_position=(
                    self.reset_position
                ),

                on_hide=self.hide,

                on_exit=self.close
            )
        )

        # =================================================
        # EVENTS
        # =================================================

        self._bind_events()

        # =================================================
        # INITIALIZE
        # =================================================

        self._initialize()

    # =====================================================
    # INITIALIZE
    # =====================================================

    def _initialize(self):

        # -------------------------------------------------
        # Load animations
        # -------------------------------------------------

        self.renderer.load_all()

        # -------------------------------------------------
        # Load saved position
        # -------------------------------------------------

        saved_position, rotation = (
            self.position_manager.load()
        )

        if rotation not in self.ROTATIONS:
            rotation = 0

        self.rotation = rotation

        # -------------------------------------------------
        # First frame
        # -------------------------------------------------

        first_frame = self.renderer.get_frame(
            "ideal",
            self.rotation,
            0
        )

        self.label.configure(
            image=first_frame
        )

        self.label.image = first_frame

        self.root.update_idletasks()

        self.avatar_width = (
            first_frame.width()
        )

        self.avatar_height = (
            first_frame.height()
        )

        # -------------------------------------------------
        # Position
        # -------------------------------------------------

        if saved_position:

            self.x, self.y = saved_position

        else:

            (
                virtual_x,
                virtual_y,
                virtual_width,
                virtual_height
            ) = self.get_virtual_screen()

            self.x = (
                virtual_x
                + virtual_width
                - self.avatar_width
                - 50
            )

            self.y = (
                virtual_y
                + virtual_height
                - self.avatar_height
                - 50
            )

        self.x, self.y = (
            self.clamp_position(
                self.x,
                self.y
            )
        )

        # -------------------------------------------------
        # Window
        # -------------------------------------------------

        self.root.geometry(
            f"{self.avatar_width}x"
            f"{self.avatar_height}"
            f"+{self.x}+{self.y}"
        )

        self.root.update_idletasks()

        # -------------------------------------------------
        # Windows handle
        # -------------------------------------------------

        self.hwnd = self.root.winfo_id()

        # -------------------------------------------------
        # Startup interaction state
        # -------------------------------------------------

        # Move Avatar starts ENABLED
        self.set_move_mode(True)

        # -------------------------------------------------
        # Synchronize context menu
        # -------------------------------------------------

        self.context_menu.set_move_avatar(
            True
        )

        self.context_menu.set_click_through(
            False
        )

        self.context_menu.set_rotation(
            self.rotation
        )

        # -------------------------------------------------
        # Tray
        # -------------------------------------------------

        self.tray = TrayManager(
            on_show=self.show,
            on_hide=self.hide,
            on_move=self.set_move_mode,
            on_reset_position=self.reset_position,
            on_exit=self.close
        )

        self.tray.start()

        # -------------------------------------------------
        # Animation
        # -------------------------------------------------

        self.player.play(
            "ideal"
        )

        self.player.start()

    # =====================================================
    # WINDOWS STYLE
    # =====================================================

    def get_exstyle(self):

        return ctypes.windll.user32.GetWindowLongW(
            self.hwnd,
            self.GWL_EXSTYLE
        )

    def set_exstyle(self, style):

        ctypes.windll.user32.SetWindowLongW(
            self.hwnd,
            self.GWL_EXSTYLE,
            style
        )

    # =====================================================
    # CLICK THROUGH
    # =====================================================

    def set_click_through(self, enabled):

        self.click_through = enabled

        if not self.hwnd:
            return

        style = self.get_exstyle()

        if enabled:

            style |= (
                self.WS_EX_TRANSPARENT
                | self.WS_EX_NOACTIVATE
            )

        else:

            style &= ~(
                self.WS_EX_TRANSPARENT
                | self.WS_EX_NOACTIVATE
            )

        self.set_exstyle(
            style
        )

        self.context_menu.set_click_through(
            enabled
        )

    # =====================================================
    # MOVE MODE
    # =====================================================

    def set_move_mode(self, enabled):

        self.move_mode = bool(
            enabled
        )

        if self.move_mode:

            # Moving requires mouse interaction
            self.set_click_through(
                False
            )

        else:

            # Normal avatar mode
            self.set_click_through(
                True
            )

        self.context_menu.set_move_avatar(
            self.move_mode
        )

        if self.tray:

            self.tray.set_move_enabled(
                self.move_mode
            )

    # =====================================================
    # MOUSE EVENTS
    # =====================================================

    def _bind_events(self):

        self.label.bind(
            "<ButtonPress-1>",
            self.start_drag
        )

        self.label.bind(
            "<B1-Motion>",
            self.drag
        )

        self.label.bind(
            "<ButtonRelease-1>",
            self.stop_drag
        )

        self.label.bind(
            "<Button-3>",
            self.show_context_menu
        )

    # =====================================================
    # CONTEXT MENU
    # =====================================================

    def show_context_menu(self, event):

        self.context_menu.show(
            event.x_root,
            event.y_root
        )

    # =====================================================
    # DRAG START
    # =====================================================

    def start_drag(self, event):

        if not self.move_mode:
            return

        self.dragging = True

        self.drag_offset_x = (
            event.x_root
            - self.root.winfo_x()
        )

        self.drag_offset_y = (
            event.y_root
            - self.root.winfo_y()
        )

    # =====================================================
    # DRAG
    # =====================================================

    def drag(self, event):

        if not self.move_mode:
            return

        if not self.dragging:
            return

        new_x = (
            event.x_root
            - self.drag_offset_x
        )

        new_y = (
            event.y_root
            - self.drag_offset_y
        )

        self.x, self.y = (
            self.clamp_position(
                new_x,
                new_y
            )
        )

        self.root.geometry(
            f"+{self.x}+{self.y}"
        )

    # =====================================================
    # DRAG STOP
    # =====================================================

    def stop_drag(self, event):

        if not self.move_mode:
            return

        self.dragging = False

        self.save_position()

    # =====================================================
    # FRAME
    # =====================================================

    def show_frame(self):

        frame = self.renderer.get_frame(
            self.animation,
            self.rotation,
            self.player.frame_index
        )

        self.label.configure(
            image=frame
        )

        self.label.image = frame

    # =====================================================
    # ROTATION
    # =====================================================

    def set_rotation(self, angle):

        if angle not in self.ROTATIONS:
            return

        self.rotation = angle

        self.update_window_size()

        self.show_frame()

        self.save_position()

        self.context_menu.set_rotation(
            angle
        )

    # =====================================================
    # WINDOW SIZE
    # =====================================================

    def update_window_size(self):

        frame = self.renderer.get_frame(
            self.animation,
            self.rotation,
            self.player.frame_index
        )

        new_width = frame.width()
        new_height = frame.height()

        center_x = (
            self.x
            + self.avatar_width / 2
        )

        center_y = (
            self.y
            + self.avatar_height / 2
        )

        self.avatar_width = new_width
        self.avatar_height = new_height

        self.x = int(
            center_x
            - new_width / 2
        )

        self.y = int(
            center_y
            - new_height / 2
        )

        self.x, self.y = (
            self.clamp_position(
                self.x,
                self.y
            )
        )

        self.root.geometry(
            f"{self.avatar_width}x"
            f"{self.avatar_height}"
            f"+{self.x}+{self.y}"
        )

    # =====================================================
    # VIRTUAL SCREEN
    # =====================================================

    def get_virtual_screen(self):

        user32 = ctypes.windll.user32

        return (
            user32.GetSystemMetrics(
                self.SM_XVIRTUALSCREEN
            ),
            user32.GetSystemMetrics(
                self.SM_YVIRTUALSCREEN
            ),
            user32.GetSystemMetrics(
                self.SM_CXVIRTUALSCREEN
            ),
            user32.GetSystemMetrics(
                self.SM_CYVIRTUALSCREEN
            )
        )

    # =====================================================
    # BOUNDS
    # =====================================================

    def clamp_position(self, x, y):

        (
            virtual_x,
            virtual_y,
            virtual_width,
            virtual_height
        ) = self.get_virtual_screen()

        margin = 10

        min_x = (
            virtual_x
            - self.avatar_width
            + margin
        )

        max_x = (
            virtual_x
            + virtual_width
            - margin
        )

        min_y = (
            virtual_y
            - self.avatar_height
            + margin
        )

        max_y = (
            virtual_y
            + virtual_height
            - margin
        )

        return (
            int(
                max(
                    min_x,
                    min(x, max_x)
                )
            ),
            int(
                max(
                    min_y,
                    min(y, max_y)
                )
            )
        )

    # =====================================================
    # POSITION SAVE
    # =====================================================

    def save_position(self):

        self.position_manager.save(
            self.root.winfo_x(),
            self.root.winfo_y(),
            self.rotation
        )

    # =====================================================
    # RESET POSITION
    # =====================================================

    def reset_position(self):

        (
            virtual_x,
            virtual_y,
            virtual_width,
            virtual_height
        ) = self.get_virtual_screen()

        self.x = (
            virtual_x
            + virtual_width
            - self.avatar_width
            - 50
        )

        self.y = (
            virtual_y
            + virtual_height
            - self.avatar_height
            - 50
        )

        self.x, self.y = (
            self.clamp_position(
                self.x,
                self.y
            )
        )

        self.root.geometry(
            f"+{self.x}+{self.y}"
        )

        self.save_position()

    # =====================================================
    # HIDE
    # =====================================================

    def hide(self):

        self.root.withdraw()

        if self.tray:

            self.tray.set_avatar_visible(
                False
            )

    # =====================================================
    # SHOW
    # =====================================================

    def show(self):

        self.root.deiconify()

        self.root.attributes(
            "-topmost",
            True
        )

        if self.tray:

            self.tray.set_avatar_visible(
                True
            )

    # =====================================================
    # PLAY
    # =====================================================

    def play(self, animation):

        self.animation = animation

        self.player.play(
            animation
        )

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.save_position()

        self.player.stop()

        if self.tray:

            self.tray.stop()

        self.renderer.close()

        self.root.destroy()

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        self.root.mainloop()