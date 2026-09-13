import asyncio
import tempfile

import edge_tts
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


class VoiceEngine:

    VOICES = {
        "en": "en-IN-NeerjaNeural",
        "hi": "hi-IN-SwaraNeural",
        "te": "te-IN-ShrutiNeural",
    }

    def __init__(
        self,
        language="en",
        avatar=None
    ):

        if language not in self.VOICES:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        self.language = language
        self.voice = self.VOICES[language]

        self.enabled = True


        # AvatarOverlay instance
        self.avatar = avatar

        pygame.mixer.init()

    def set_enabled(self, enabled):

        self.enabled = enabled

    # =====================================================
    # LANGUAGE
    # =====================================================

    def set_language(self, language):

        if language not in self.VOICES:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        self.language = language
        self.voice = self.VOICES[language]

    # =====================================================
    # AVATAR ANIMATION
    # =====================================================

    def _avatar_animation(self, animation):

        if self.avatar is None:
            return

        try:

            self.avatar.root.after(
                0,
                self.avatar.play,
                animation
            )

        except Exception:
            pass

    # =====================================================
    # GENERATE SPEECH
    # =====================================================

    async def _generate(
        self,
        text,
        filename
    ):

        communicate = edge_tts.Communicate(
            text,
            self.voice
        )

        await communicate.save(
            filename
        )

    # =====================================================
    # SPEAK
    # =====================================================

    def speak(self, text):

        if not self.enabled:
            return

        if not text:
            return

        temp_file = tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False
        )

        temp_file.close()

        filename = temp_file.name

        try:

            # ---------------------------------------------
            # Generate audio FIRST
            # ---------------------------------------------

            asyncio.run(
                self._generate(
                    text,
                    filename
                )
            )

            # ---------------------------------------------
            # Load audio FIRST
            # ---------------------------------------------

            pygame.mixer.music.load(
                filename
            )

            # ---------------------------------------------
            # START BOTH AT THE SAME TIME
            # ---------------------------------------------

            self._avatar_animation(
                "talking"
            )

            pygame.mixer.music.play()

            # ---------------------------------------------
            # Wait for voice to finish
            # ---------------------------------------------

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(30)

        finally:

            # ---------------------------------------------
            # Voice finished → ideal animation
            # ---------------------------------------------

            self._avatar_animation(
                "ideal"
            )

            # ---------------------------------------------
            # Cleanup
            # ---------------------------------------------

            try:
                pygame.mixer.music.unload()

            except Exception:
                pass

            try:
                os.remove(filename)

            except Exception:
                pass

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        try:

            pygame.mixer.music.stop()

            pygame.mixer.quit()

        except Exception:
            pass