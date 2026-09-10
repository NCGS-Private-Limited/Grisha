import re


class WakeWordEngine:

    # =====================================================
    # WAKE WORDS
    # =====================================================

    WAKE_WORDS = (
        "hey grisha",
        "hi grisha",
        "hello grisha",
        "grisha",

        # Common Whisper variations
        "gresha",
        "greesha",
        "grishaah",
        "greshaah",
        "grecia",
    )

    def __init__(self):
        self.enabled = True

    # =====================================================
    # NORMALIZE
    # =====================================================

    @staticmethod
    def normalize(text):

        if not text:
            return ""

        text = text.lower()

        # Remove punctuation
        text = re.sub(
            r"[^\w\s]",
            " ",
            text
        )

        # Remove duplicate spaces
        text = " ".join(
            text.split()
        )

        return text

    # =====================================================
    # CHECK
    # =====================================================

    def is_wake_word(self, text):

        if not self.enabled:
            return False

        text = self.normalize(text)

        if not text:
            return False

        # Exact match
        if text in self.WAKE_WORDS:
            return True

        # Allow wake word inside a short phrase
        words = text.split()

        for wake_word in self.WAKE_WORDS:

            wake_words = wake_word.split()

            if len(wake_words) <= len(words):

                for i in range(
                    len(words) - len(wake_words) + 1
                ):

                    candidate = " ".join(
                        words[
                            i:i + len(wake_words)
                        ]
                    )

                    if candidate == wake_word:
                        return True

        return False

    # =====================================================
    # EXTRACT COMMAND
    # =====================================================

    def remove_wake_word(self, text):

        text = self.normalize(text)

        if not text:
            return ""

        # Longest phrases first
        wake_words = sorted(
            self.WAKE_WORDS,
            key=len,
            reverse=True
        )

        for wake_word in wake_words:

            pattern = (
                r"^"
                + re.escape(wake_word)
                + r"\b"
            )

            if re.match(pattern, text):

                command = re.sub(
                    pattern,
                    "",
                    text,
                    count=1
                )

                return " ".join(
                    command.split()
                )

        return text