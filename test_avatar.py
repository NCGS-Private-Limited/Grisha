import tkinter as tk
from pathlib import Path

from avatar import AvatarPlayer


BASE_DIR = Path(__file__).parent

ANIMATIONS_DIR = (
    BASE_DIR
    / "avatar"
    / "animations"
)


root = tk.Tk()

root.title("Grisha Avatar Player")

root.geometry("800x600")

label = tk.Label(
    root,
    bg="gray20"
)

label.pack(
    expand=True
)


avatar = AvatarPlayer(
    animations_dir=ANIMATIONS_DIR,
    fps=24,
    scale=0.4,
    cache_size=12,
)

avatar.play("ideal_transparent")


def update():
    if avatar.update():

        frame = avatar.get_current_tk_frame()

        if frame is not None:
            label.configure(image=frame)
            label.image = frame

    root.after(1, update)


def start_talking(event=None):
    avatar.play("talking_transparent")


def start_idle(event=None):
    avatar.play("ideal_transparent")


root.bind("<space>", start_talking)
root.bind("<Return>", start_idle)


def on_close():
    avatar.release()
    root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)

update()

root.mainloop()