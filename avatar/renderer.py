from pathlib import Path

from PIL import Image, ImageTk


class AvatarRenderer:

    ROTATIONS = (0, 90, 180, 270)

    def __init__(
        self,
        animations_dir,
        scale=0.25
    ):
        self.animations_dir = Path(
            animations_dir
        )

        self.scale = scale

        self.images = {}
        self.rotated_images = {}
        self.tk_frames = {}

    # =====================================================
    # LOAD
    # =====================================================

    def load_animation(
        self,
        animation_name
    ):
        directory = (
            self.animations_dir
            / f"{animation_name}_transparent"
        )

        paths = sorted(
            directory.glob("*.png")
        )

        if not paths:
            raise FileNotFoundError(
                f"No PNG frames found:\n{directory}"
            )

        frames = []

        for index, path in enumerate(
            paths,
            1
        ):
            image = Image.open(
                path
            ).convert("RGBA")

            width, height = image.size

            width = int(
                width * self.scale
            )

            height = int(
                height * self.scale
            )

            image = image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            frames.append(image)

        self.images[animation_name] = frames

    # =====================================================
    # ROTATION CACHE
    # =====================================================

    def build_rotation_cache(
        self,
        animation_name
    ):
        if animation_name not in self.images:
            self.load_animation(
                animation_name
            )

        self.rotated_images[
            animation_name
        ] = {}

        self.tk_frames[
            animation_name
        ] = {}

        for rotation in self.ROTATIONS:

            rotated_frames = []
            tk_animation = []

            for image in self.images[
                animation_name
            ]:

                if rotation == 0:
                    rotated = image.copy()

                else:
                    rotated = image.rotate(
                        rotation,
                        expand=True,
                        resample=Image.Resampling.BICUBIC
                    )

                rotated_frames.append(
                    rotated
                )

                tk_animation.append(
                    ImageTk.PhotoImage(
                        rotated
                    )
                )

            self.rotated_images[
                animation_name
            ][rotation] = rotated_frames

            self.tk_frames[
                animation_name
            ][rotation] = tk_animation

    # =====================================================
    # LOAD ALL
    # =====================================================

    def load_all(self):

        for animation in (
            "ideal",
            "talking"
        ):
            self.load_animation(
                animation
            )

        for animation in (
            "ideal",
            "talking"
        ):
            self.build_rotation_cache(
                animation
            )

    # =====================================================
    # GET FRAME
    # =====================================================

    def get_frame(
        self,
        animation,
        rotation,
        index
    ):
        return self.tk_frames[
            animation
        ][rotation][index]

    # =====================================================
    # FRAME COUNT
    # =====================================================

    def frame_count(
        self,
        animation
    ):
        return len(
            self.tk_frames[
                animation
            ][0]
        )

    # =====================================================
    # SIZE
    # =====================================================

    def get_size(
        self,
        animation,
        rotation,
        index=0
    ):
        frame = self.get_frame(
            animation,
            rotation,
            index
        )

        return (
            frame.width(),
            frame.height()
        )

    # =====================================================
    # CLEANUP
    # =====================================================

    def close(self):

        for animation in self.rotated_images:

            for rotation in self.rotated_images[
                animation
            ]:

                for image in self.rotated_images[
                    animation
                ][rotation]:

                    image.close()

        self.images.clear()
        self.rotated_images.clear()
        self.tk_frames.clear()