import requests
import json
from helpers.decorators import log_data
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import time


URL = "https://coqui-tts-gpu-901342520595.us-central1.run.app/synthesize"
SECRETS = "secrets.json"
LOCAL_AUDIO = "output.wav"
TEST_TEXT = "Herb node is spotted!"


def get_gcp_token():
    try:
        with open(SECRETS) as f:
            data = json.load(f)
            return data["GCP_TOKEN"]
    except Exception as e:
        print("Error: ", e)


def get_eleven_labs_token():
    try:
        with open(SECRETS) as f:
            data = json.load(f)
            return data["ELEVEN_LABS_API_KEY"]
    except Exception as e:
        print("Error: ", e)


@log_data
def run_gcp_api(text: str) -> None:
    params = {"text": text, "dest": LOCAL_AUDIO}
    headers = {'Authorization': f"Bearer {get_gcp_token()}"}
    response = requests.post(URL, headers=headers, params=params)
    response.raise_for_status()
    with open(LOCAL_AUDIO, "wb") as f:
        f.write(response.content)


@log_data
def run_eleven_labs_api(text: str) -> None:
    client = ElevenLabs(
        api_key=get_eleven_labs_token()
    )

    audio = client.generate(
        text=text,
        voice="Brian",
        model="eleven_multilingual_v2"
    )
    save(audio, LOCAL_AUDIO)


def main():
    n = 1
    gcp_times = []
    eleven_labs_times = []
    for _ in range(n):
        s = time.time()
        run_gcp_api(TEST_TEXT)
        e = time.time()
        gcp_times.append(e - s)
        s = time.time()
        run_eleven_labs_api(TEST_TEXT)
        e = time.time()
        eleven_labs_times.append(e - s)
    print(gcp_times)
    print()
    print(eleven_labs_times)


if __name__ == "__main__":
    main()
