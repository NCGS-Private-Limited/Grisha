import os
import sys
import glob
import ctypes
import time

# =====================================================
# CURRENT PYTHON
# =====================================================

print("Python:")
print(sys.executable)

# =====================================================
# FIND SITE-PACKAGES CORRECTLY
# =====================================================

site_packages = next(
    path
    for path in sys.path
    if path.endswith(
        os.path.join("Lib", "site-packages")
    )
    and os.path.isdir(path)
)

BASE = os.path.join(
    site_packages,
    "nvidia"
)

print("\nSite-packages:")
print(site_packages)

print("\nNVIDIA root:")
print(BASE)

# =====================================================
# ADD ALL NVIDIA DLL DIRECTORIES
# =====================================================

dll_handles = []

for bin_dir in glob.glob(
    os.path.join(BASE, "*", "bin")
):

    print(
        f"\nAdding DLL directory: {bin_dir}"
    )

    if os.path.isdir(bin_dir):

        dll_handles.append(
            os.add_dll_directory(bin_dir)
        )

        os.environ["PATH"] = (
            bin_dir
            + os.pathsep
            + os.environ["PATH"]
        )

# =====================================================
# TEST cuBLAS
# =====================================================

print("\nTesting cuBLAS...")

cublas = os.path.join(
    BASE,
    "cublas",
    "bin",
    "cublas64_12.dll"
)

print("DLL:")
print(cublas)

print(
    "Exists:",
    os.path.exists(cublas)
)

if not os.path.exists(cublas):
    raise FileNotFoundError(
        "cuBLAS DLL was not found."
    )

ctypes.WinDLL(cublas)

print(
    "cuBLAS loaded successfully!"
)

# =====================================================
# TEST CTRANSLATE2
# =====================================================

print("\nTesting CTranslate2...")

import ctranslate2

print(
    "CTranslate2:",
    ctranslate2.__version__
)

print(
    "CUDA devices:",
    ctranslate2.get_cuda_device_count()
)

print(
    "CUDA types:",
    ctranslate2.get_supported_compute_types(
        "cuda"
    )
)

print(
    "\nCUDA environment test PASSED"
)

print("\nTesting Whisper GPU inference...")

import numpy as np
from faster_whisper import WhisperModel

print("Loading Whisper...")

model = WhisperModel(
    "base",
    device="cuda",
    compute_type="float16"
)

print("Whisper loaded.")

print("\nRecording 5 seconds...")

import sounddevice as sd

audio = sd.rec(
    5 * 16000,
    samplerate=16000,
    channels=1,
    dtype="float32",
    device=1
)

sd.wait()

audio = np.squeeze(audio)

print("Recording finished.")
print("Transcribing...")

start = time.perf_counter()

segments, info = model.transcribe(
    audio,
    language="en",
    beam_size=5
)

text = " ".join(
    segment.text.strip()
    for segment in segments
)

elapsed = time.perf_counter() - start

print("\n==============================")
print("WHISPER GPU RESULT")
print("==============================")

print("Text:", text)
print("Language:", info.language)
print(f"Processing time: {elapsed:.2f}s")

print("==============================")