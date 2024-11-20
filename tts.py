import torch
from TTS.api import TTS
import time

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
# print(TTS().list_models())

# Init TTS
s = time.time()
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
e = time.time()
print(e - s)

speaker_wav = "HO_03_female0_en.wav"


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
    print(e - s)
    return file_path


def text_to_speech_stream(
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
    print(e - s)
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
