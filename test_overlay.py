from avatar.overlay import AvatarOverlay


def main():

    print()
    print("======================================")
    print("       GRISHA F2 AVATAR TEST")
    print("======================================")
    print()

    avatar = AvatarOverlay()

    print("Avatar loaded.")
    print()
    print("Right-click the avatar for the menu.")
    print()
    print("Menu:")
    print("  Move Avatar")
    print("  Click-through")
    print("  Rotation")
    print("  Reset Position")
    print("  Hide Avatar")
    print("  Exit Grisha")
    print()

    avatar.run()


if __name__ == "__main__":
    main()