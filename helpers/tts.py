import torch
from TTS.api import TTS
import time
import sys
import os
from decorators import log_data

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

USE_GPU = device == "cuda"

LOCAL_PATH = "~/.local/share/tts/tts_models/multilingual/multi-dataset/xtts_v2/"
# LOCAL_PATH_DOCKER = "/root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2"
LOCAL_PATH_DOCKER = "/root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2"


# List available 🐸TTS models
# print(TTS().list_models())
print(device)

# Init TTS
s = time.time()
# cache_dir = os.path.expanduser(LOCAL_PATH_DOCKER)
# if os.path.isdir(LOCAL_PATH_DOCKER):
#     print("Model file exists")
#     tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
# else:
#     print("CANNOT FIND MODEL FILE")
#     tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
if os.path.isdir(LOCAL_PATH_DOCKER):
    # Model is already downloaded, use local path
    print("Model directory found, loading from local path.")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
else:
    # Fallback: use the friendly name (which may trigger a download)
    print("Local model directory not found, downloading model at runtime.")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
# tts = TTS(LOCAL_PATH_DOCKER)
# tts = TTS(
#     checkpoint_path="/root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/model.pth",
#     config_path="/root/.local/share/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json",
#     gpu=USE_GPU
# )
e = time.time()
size_in_bytes = sys.getsizeof(tts)
print(f"Time to load model in memory: {e - s}")
print(f"TTS size in bytes: {size_in_bytes}")


speaker_wav = "helpers/HO_03_female0_en.wav"


@log_data
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


# Issue I am running into: Needs to load a new model for every inference,
# but this is slow need to figure out how to only load model once?
# https://coqui-tts.readthedocs.io/en/latest/models/xtts.html#id5

# Lets just start with creating audio files, then move to streaming.

# Maybe I should just store the data directly into the cloud, and return a
# bucket address?


def main():
    pass


if __name__ == "__main__":
    main()
