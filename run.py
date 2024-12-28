import requests
import json
from helpers.decorators import log_data

URL = "https://coqui-tts-gpu-901342520595.us-central1.run.app/synthesize"
SECRETS = "secrets.json"
LOCAL_AUDIO = "output.wav"
TEST_TEXT = "Very nice! It seems inference speed is fast again."


def get_gcp_token():
    try:
        with open(SECRETS) as f:
            data = json.load(f)
            return data["GCP_TOKEN"]
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


def main():
    run_gcp_api(TEST_TEXT)


if __name__ == "__main__":
    main()
