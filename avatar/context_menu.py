import tkinter as tk


class AvatarContextMenu:

    def __init__(
        self,
        root,
        on_move=None,
        on_click_through_toggle=None,
        on_rotation=None,
        on_reset_position=None,
        on_hide=None,
        on_exit=None
    ):
        self.root = root

        self.on_move = on_move
        self.on_click_through_toggle = (
            on_click_through_toggle
        )
        self.on_rotation = on_rotation
        self.on_reset_position = (
            on_reset_position
        )
        self.on_hide = on_hide
        self.on_exit = on_exit

        self.move_avatar_var = tk.BooleanVar(
            value=False
        )

        self.click_through_var = tk.BooleanVar(
            value=True
        )

        self.rotation_var = tk.IntVar(
            value=0
        )

        self.menu = tk.Menu(
            root,
            tearoff=False
        )

        self._build()

    def _build(self):

        self.menu.add_checkbutton(
            label="Move Avatar",
            variable=self.move_avatar_var,
            command=self._toggle_move
        )

        self.menu.add_checkbutton(
            label="Click-through",
            variable=self.click_through_var,
            command=self._toggle_click_through
        )

        self.menu.add_separator()

        rotation_menu = tk.Menu(
            self.menu,
            tearoff=False
        )

        for angle in (
            0,
            90,
            180,
            270
        ):
            rotation_menu.add_radiobutton(
                label=f"{angle}°",
                value=angle,
                variable=self.rotation_var,
                command=lambda a=angle:
                    self._rotate(a)
            )

        self.menu.add_cascade(
            label="Rotation",
            menu=rotation_menu
        )

        self.menu.add_separator()

        self.menu.add_command(
            label="Reset Position",
            command=self._reset_position
        )

        self.menu.add_command(
            label="Hide Avatar",
            command=self._hide
        )

        self.menu.add_separator()

        self.menu.add_command(
            label="Exit Grisha",
            command=self._exit
        )

    def show(self, x, y):

        try:
            self.menu.tk_popup(
                x,
                y
            )
        finally:
            self.menu.grab_release()

    def _toggle_move(self):

        enabled = self.move_avatar_var.get()

        if self.on_move:
            self.on_move(enabled)

    def _toggle_click_through(self):

        enabled = (
            self.click_through_var.get()
        )

        if self.on_click_through_toggle:
            self.on_click_through_toggle(
                enabled
            )

    def _rotate(self, angle):

        self.rotation_var.set(
            angle
        )

        if self.on_rotation:
            self.on_rotation(
                angle
            )

    def _reset_position(self):

        if self.on_reset_position:
            self.on_reset_position()

    def _hide(self):

        if self.on_hide:
            self.on_hide()

    def _exit(self):

        if self.on_exit:
            self.on_exit()

    def set_move_avatar(self, enabled):

        self.move_avatar_var.set(
            enabled
        )

    def set_click_through(self, enabled):

        self.click_through_var.set(
            enabled
        )

    def set_rotation(self, angle):

        self.rotation_var.set(
            angle
        )