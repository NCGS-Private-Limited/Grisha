from avatar.overlay import AvatarOverlay


def main():

    avatar = AvatarOverlay()

    # ---------------------------------------------
    # Show test dialog
    # ---------------------------------------------

    avatar.root.after(
        1000,
        avatar.show_dialog,
        "Hello, I am Grisha. This is a dialog test."
    )

    # ---------------------------------------------
    # Hide after 5 seconds
    # ---------------------------------------------

    avatar.root.after(
        6000,
        avatar.hide_dialog
    )

    # ---------------------------------------------
    # Show another dialog after 7 seconds
    # ---------------------------------------------

    avatar.root.after(
        7000,
        avatar.show_dialog,
        "The dialog stays straight even when I rotate."
    )

    # ---------------------------------------------
    # Keep it visible for 5 seconds
    # ---------------------------------------------

    avatar.root.after(
        12000,
        avatar.hide_dialog
    )

    # ---------------------------------------------
    # Close test after 13 seconds
    # ---------------------------------------------

    avatar.root.after(
        13000,
        avatar.close
    )

    # ---------------------------------------------
    # Start avatar
    # ---------------------------------------------

    avatar.run()


if __name__ == "__main__":
    main()