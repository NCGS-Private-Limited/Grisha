import os
import sys
import glob
import threading

# =====================================================
# NVIDIA CUDA DLL SETUP
# =====================================================

def setup_cuda():

    site_packages = next(
        path
        for path in sys.path
        if path.endswith(
            os.path.join("Lib", "site-packages")
        )
        and os.path.isdir(path)
    )

    nvidia_root = os.path.join(
        site_packages,
        "nvidia"
    )

    dll_handles = []

    if os.path.isdir(nvidia_root):

        for bin_dir in glob.glob(
            os.path.join(
                nvidia_root,
                "*",
                "bin"
            )
        ):

            if os.path.isdir(bin_dir):

                dll_handles.append(
                    os.add_dll_directory(
                        bin_dir
                    )
                )

                os.environ["PATH"] = (
                    bin_dir
                    + os.pathsep
                    + os.environ["PATH"]
                )

    return dll_handles


# IMPORTANT:
# CUDA DLLs must be initialized BEFORE
# importing/using faster-whisper.

_DLL_HANDLES = setup_cuda()


# =====================================================
# NORMAL IMPORTS
# =====================================================

import sounddevice as sd
import numpy as np

from faster_whisper import WhisperModel


class STTEngine:

    def __init__(
        self,
        language="en",
        model_size="base",
        mic_device=1
    ):

        self.language = language
        self.model_size = model_size
        self.mic_device = mic_device

        self.sample_rate = 16000
        self.channels = 1
        self.record_seconds = 5

        self.stop_event = threading.Event()

        self.wake_words = (
            "grisha",
            "hey grisha",
            "hi grisha",
            "hey grisha",
            "he grisha",
        )

        print("Loading STT...")

        self.model = WhisperModel(
            self.model_size,
            device="cuda",
            compute_type="float16"
        )

        print("STT ready.")

    # =================================================
    # LANGUAGE
    # =================================================

    def set_language(self, language):

        self.language = language

    # =================================================
    # LISTEN
    # =================================================

    def listen(self):

        if self.stop_event.is_set():
            return ""

        print("Listening...")

        audio = sd.rec(
            int(
                self.record_seconds
                * self.sample_rate
            ),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            device=self.mic_device
        )

        sd.wait()

        audio = np.squeeze(audio)

        print("Processing...")

        segments, info = self.model.transcribe(
            audio,
            language=self.language,
            beam_size=5
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        # =================================================
        # CLEAN STT OUTPUT
        # =================================================

        text = text.replace(",", " ")
        text = text.replace(".", "")
        text = text.strip()

        text = text.strip()

        print(
            f"Heard: {text}"
        )

        return text

    # =================================================
    # WAIT FOR WAKE WORD
    # =================================================

    def wait_for_wake_word(self):

        while not self.stop_event.is_set():

            print("Waiting for wake word...", end="\r")

            audio = sd.rec(
                int(1 * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                device=self.mic_device
            )

            sd.wait()

            audio = np.squeeze(audio)

            segments, info = self.model.transcribe(
                audio,
                language=self.language,
                beam_size=1
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
            )

            text = text.lower()

            text = text.replace(",", " ")
            text = text.replace(".", "")
            text = text.replace("!", "")
            text = text.strip()

            for wake_word in self.wake_words:

                if wake_word in text:
                    print("Wake word detected!     ")

                    return True

    # =================================================
    # CLOSE
    # =================================================

    def close(self):

        pass

    # =================================================
    # STOP STT
    # =================================================

    def stop(self):

        self.stop_event.set()

    # =================================================
    # RESUME STT
    # =================================================

    def resume(self):

        self.stop_event.clear()

    # =================================================
    # CHECK STATUS
    # =================================================

    def is_stopped(self):

        return self.stop_event.is_set()