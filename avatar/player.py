class AvatarPlayer:

    def __init__(
        self,
        root,
        renderer,
        show_frame,
        fps=24,
        ideal_speed=1.5,
        talking_speed=1.15,
        ideal_hold=2.0
    ):
        self.root = root
        self.renderer = renderer
        self.show_frame = show_frame

        self.fps = fps
        self.ideal_speed = ideal_speed
        self.talking_speed = talking_speed
        self.ideal_hold = ideal_hold

        self.animation = "ideal"
        self.frame_index = 0
        self.ideal_holding = True

        self.running = False
        self.after_id = None

    def play(self, animation):

        if animation not in (
            "ideal",
            "talking"
        ):
            raise ValueError(
                f"Unknown animation: {animation}"
            )

        self.animation = animation
        self.frame_index = 0

        self.ideal_holding = (
            animation == "ideal"
        )

        self.show_frame()

    def start(self):

        if self.running:
            return

        self.running = True
        self._next_frame()

    def stop(self):

        self.running = False

        if self.after_id is not None:

            self.root.after_cancel(
                self.after_id
            )

            self.after_id = None

    def _schedule(self, delay):

        self.after_id = self.root.after(
            delay,
            self._next_frame
        )

    def _next_frame(self):

        if not self.running:
            return

        if self.animation == "ideal":

            if self.ideal_holding:

                self.frame_index = 0

                self.show_frame()

                self.ideal_holding = False

                self._schedule(
                    int(
                        self.ideal_hold * 1000
                    )
                )

                return

            self.frame_index += 1

            if self.frame_index >= (
                self.renderer.frame_count(
                    "ideal"
                )
            ):

                self.frame_index = 0
                self.ideal_holding = True

                self.show_frame()

                self._schedule(
                    int(
                        self.ideal_hold * 1000
                    )
                )

                return

            self.show_frame()

            fps = (
                self.fps
                * self.ideal_speed
            )

            self._schedule(
                max(
                    1,
                    int(1000 / fps)
                )
            )

            return

        # TALKING

        self.show_frame()

        self.frame_index += 1

        if self.frame_index >= (
            self.renderer.frame_count(
                "talking"
            )
        ):
            self.frame_index = 0

        fps = (
            self.fps
            * self.talking_speed
        )

        self._schedule(
            max(
                1,
                int(1000 / fps)
            )
        )