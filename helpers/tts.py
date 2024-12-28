import torch
from TTS.api import TTS
import time
import sys
import os

# Get device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
USE_GPU = DEVICE == "cuda"
MODEL_NAME = "tts_models--multilingual--multi-dataset--xtts_v2"
MODEL_NAME_DASHES = "tts_models/multilingual/multi-dataset/xtts_v2"
MODEL_PATH = "/root/.local/share/tts"
LOCAL_PATH_DOCKER = f"{MODEL_PATH}/{MODEL_NAME}"
print(DEVICE)

s = time.time()
if os.path.isdir(LOCAL_PATH_DOCKER):
    print("Model directory found, loading from local path.")
else:
    print("Local model directory not found, downloading model at runtime.")
tts = TTS(MODEL_NAME_DASHES).to(DEVICE)

e = time.time()
size_in_bytes = sys.getsizeof(tts)
print(f"Time to load model in memory: {e - s}")
print(f"TTS size in bytes: {size_in_bytes}")


speaker_wav = "helpers/HO_03_female0_en.wav"


def text_to_speech(
        text: str, 
        speaker_wav: str = speaker_wav,
        model=tts,
        file_path: str = "output.wav") -> str:
    """Takes in a string, generates an audio wav, returns wav filepath"""
    s = time.time()
    model.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="en",
        file_path=file_path
    )
    e = time.time()
    print(f"Time for inference: {e - s}")
    return file_path


def main():
    pass


if __name__ == "__main__":
    main()
