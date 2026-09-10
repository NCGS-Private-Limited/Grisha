import tkinter as tk


class DialogManager:

    def __init__(
        self,
        root,
        get_avatar_geometry,
        get_virtual_screen
    ):

        self.root = root

        self.get_avatar_geometry = (
            get_avatar_geometry
        )

        self.get_virtual_screen = (
            get_virtual_screen
        )

        self.window = None
        self.label = None

        self.visible = False
        self.animating = False

        self.animation_id = None

        # =================================================
        # APPEARANCE
        # =================================================

        self.bg = "#202020"
        self.fg = "#FFFFFF"

        self.font = (
            "Segoe UI",
            11
        )

        self.max_width = 320

        self.padding_x = 14
        self.padding_y = 9

        self.gap = 12

        # =================================================
        # ANIMATION
        # =================================================

        self.animation_duration = 220

        self.min_alpha = 0.0
        self.max_alpha = 0.96

        self.animation_steps = 18

    # =====================================================
    # CREATE WINDOW
    # =====================================================

    def _create_window(self):

        if self.window is not None:
            return

        self.window = tk.Toplevel(
            self.root
        )

        self.window.overrideredirect(
            True
        )

        self.window.attributes(
            "-topmost",
            True
        )

        self.window.attributes(
            "-alpha",
            self.min_alpha
        )

        self.window.configure(
            bg=self.bg
        )

        self.label = tk.Label(
            self.window,
            text="",
            bg=self.bg,
            fg=self.fg,
            font=self.font,
            justify="left",
            anchor="w",
            wraplength=self.max_width,
            padx=self.padding_x,
            pady=self.padding_y,
            bd=0,
            highlightthickness=0
        )

        self.label.pack()

        self.window.withdraw()

    # =====================================================
    # SHOW
    # =====================================================

    def show(self, text):

        if not text:
            return

        self._create_window()

        self._cancel_animation()

        self.label.configure(
            text=text
        )

        self.window.update_idletasks()

        self._position()

        self.window.attributes(
            "-alpha",
            self.min_alpha
        )

        self.window.deiconify()

        self.window.lift()

        self.visible = True

        self._ease_in()

    # =====================================================
    # HIDE
    # =====================================================

    def hide(self):

        if (
            self.window is None
            or not self.visible
        ):
            return

        self._cancel_animation()

        self._ease_out()

    # =====================================================
    # UPDATE POSITION
    # =====================================================

    def update_position(self):

        if (
            self.window is None
            or not self.visible
        ):
            return

        self._position()

    # =====================================================
    # POSITION
    # =====================================================

    def _position(self):

        if self.window is None:
            return

        (
            avatar_x,
            avatar_y,
            avatar_width,
            avatar_height
        ) = self.get_avatar_geometry()

        (
            virtual_x,
            virtual_y,
            virtual_width,
            virtual_height
        ) = self.get_virtual_screen()

        self.window.update_idletasks()

        dialog_width = (
            self.window.winfo_reqwidth()
        )

        dialog_height = (
            self.window.winfo_reqheight()
        )

        # =================================================
        # AVATAR CENTER
        # =================================================

        avatar_center_x = (
            avatar_x
            + avatar_width // 2
        )

        # =================================================
        # PREFERRED: ABOVE
        # =================================================

        x = (
            avatar_center_x
            - dialog_width // 2
        )

        y = (
            avatar_y
            - dialog_height
            - self.gap
        )

        # =================================================
        # HORIZONTAL BOUNDARY
        # =================================================

        min_x = (
            virtual_x + 8
        )

        max_x = (
            virtual_x
            + virtual_width
            - dialog_width
            - 8
        )

        x = max(
            min_x,
            min(x, max_x)
        )

        # =================================================
        # VERTICAL BOUNDARY
        # =================================================

        top_limit = (
            virtual_y + 8
        )

        bottom_limit = (
            virtual_y
            + virtual_height
            - dialog_height
            - 8
        )

        # =================================================
        # NO ROOM ABOVE → BELOW
        # =================================================

        if y < top_limit:

            y = (
                avatar_y
                + avatar_height
                + self.gap
            )

        # =================================================
        # NO ROOM BELOW → SIDE
        # =================================================

        if y > bottom_limit:

            right_x = (
                avatar_x
                + avatar_width
                + self.gap
            )

            left_x = (
                avatar_x
                - dialog_width
                - self.gap
            )

            if (
                right_x + dialog_width
                <= virtual_x
                + virtual_width
                - 8
            ):

                x = right_x

            elif left_x >= (
                virtual_x + 8
            ):

                x = left_x

            else:

                y = max(
                    top_limit,
                    min(
                        y,
                        bottom_limit
                    )
                )

        # =================================================
        # FINAL SAFETY CLAMP
        # =================================================

        x = max(
            virtual_x + 8,
            min(
                x,
                virtual_x
                + virtual_width
                - dialog_width
                - 8
            )
        )

        y = max(
            virtual_y + 8,
            min(
                y,
                virtual_y
                + virtual_height
                - dialog_height
                - 8
            )
        )

        self.window.geometry(
            f"{dialog_width}x"
            f"{dialog_height}"
            f"+{int(x)}+{int(y)}"
        )

    # =====================================================
    # EASE-IN
    # =====================================================

    def _ease_in(self):

        if self.window is None:
            return

        self.animating = True

        self._animate_alpha(
            self.min_alpha,
            self.max_alpha,
            self._finish_show
        )

    # =====================================================
    # EASE-OUT
    # =====================================================

    def _ease_out(self):

        if self.window is None:
            return

        self.animating = True

        try:

            current_alpha = float(
                self.window.attributes(
                    "-alpha"
                )
            )

        except (
            TypeError,
            ValueError
        ):

            current_alpha = (
                self.max_alpha
            )

        self._animate_alpha(
            current_alpha,
            self.min_alpha,
            self._finish_hide
        )

    # =====================================================
    # ALPHA ANIMATION
    # =====================================================

    def _animate_alpha(
        self,
        start_alpha,
        end_alpha,
        callback
    ):

        self._cancel_animation()

        steps = self.animation_steps

        interval = max(
            1,
            self.animation_duration
            // steps
        )

        step = 0

        def animate():

            nonlocal step

            if self.window is None:
                return

            step += 1

            progress = (
                step / steps
            )

            # -----------------------------------------
            # Smoothstep easing
            #
            # 0 → 0
            # 0.5 → 0.5
            # 1 → 1
            # -----------------------------------------

            eased = (
                progress
                * progress
                * (
                    3
                    - 2 * progress
                )
            )

            alpha = (
                start_alpha
                + (
                    end_alpha
                    - start_alpha
                )
                * eased
            )

            self.window.attributes(
                "-alpha",
                alpha
            )

            if step < steps:

                self.animation_id = (
                    self.root.after(
                        interval,
                        animate
                    )
                )

            else:

                self.animation_id = None

                callback()

        animate()

    # =====================================================
    # FINISH SHOW
    # =====================================================

    def _finish_show(self):

        self.animating = False

        if self.window is not None:

            self.window.attributes(
                "-alpha",
                self.max_alpha
            )

            self.window.lift()

    # =====================================================
    # FINISH HIDE
    # =====================================================

    def _finish_hide(self):

        self.animating = False

        self.visible = False

        if self.window is not None:

            self.window.attributes(
                "-alpha",
                self.min_alpha
            )

            self.window.withdraw()

    # =====================================================
    # CANCEL
    # =====================================================

    def _cancel_animation(self):

        if self.animation_id is not None:

            try:

                self.root.after_cancel(
                    self.animation_id
                )

            except Exception:
                pass

            self.animation_id = None

        self.animating = False

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self._cancel_animation()

        if self.window is not None:

            try:
                self.window.destroy()

            except Exception:
                pass

            self.window = None
            self.label = None

        self.visible = False