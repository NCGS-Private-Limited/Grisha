import os
import sys
import glob

# ==========================================
# NVIDIA CUDA DLL setup
# ==========================================

site_packages = os.path.dirname(os.__file__)

# Get the current virtual environment's site-packages
venv_site_packages = os.path.join(
    os.path.dirname(sys.executable),
    "..",
    "Lib",
    "site-packages"
)

venv_site_packages = os.path.abspath(venv_site_packages)

nvidia_root = os.path.join(
    venv_site_packages,
    "nvidia"
)

dll_handles = []

if os.path.isdir(nvidia_root):
    for bin_dir in glob.glob(
            os.path.join(nvidia_root, "*", "bin")
    ):
        if os.path.isdir(bin_dir):
            print(f"CUDA DLL: {bin_dir}")

            # Add DLL directory for Windows DLL loading
            dll_handles.append(
                os.add_dll_directory(bin_dir)
            )

            # Also add it to PATH for native libraries
            os.environ["PATH"] = (
                    bin_dir + os.pathsep + os.environ["PATH"]
            )

# ==========================================
# Normal imports
# ==========================================

import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import time
# ==============================
# Configuration
# ==============================

MIC_DEVICE = 1
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5

MODEL_SIZE = "base"

# ==============================
# Load Whisper
# ==============================

print("=" * 50)
print("        GRISHA STT LAB V1.0")
print("=" * 50)

print("\nLoading Whisper model...")

model = WhisperModel(
    MODEL_SIZE,
    device="cuda",
    compute_type="float16"
)

print("Whisper loaded successfully.")
print(f"Model : {MODEL_SIZE}")
print("Device: CUDA")

# ==============================
# Record
# ==============================

input("\nPress ENTER to start recording...")

print("\n🎤 Recording...")

audio = sd.rec(
    int(RECORD_SECONDS * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="float32",
    device=MIC_DEVICE
)

sd.wait()

print("⏹ Recording finished.")

# ==============================
# Convert audio
# ==============================

audio = np.squeeze(audio)

# ==============================
# Transcribe
# ==============================

print("\nTranscribing...")

start_time = time.perf_counter()

segments, info = model.transcribe(
    audio,
    language="en",
    beam_size=5
)

text = " ".join(segment.text.strip() for segment in segments)

elapsed = time.perf_counter() - start_time

# ==============================
# Result
# ==============================

print("\n" + "=" * 50)
print("RESULT")
print("=" * 50)

print(f"\nText: {text}")
print(f"Language: {info.language}")
print(f"Processing time: {elapsed:.2f} seconds")

print("\n" + "=" * 50)