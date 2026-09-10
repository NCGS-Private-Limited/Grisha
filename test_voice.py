from voice import VoiceEngine


def main():

    voice = VoiceEngine(
        language="en"
    )

    print("Testing Grisha voice...")

    voice.speak(
        "Hello! I am Grisha."
    )

    print("Voice test completed.")

    voice.close()


if __name__ == "__main__":
    main()