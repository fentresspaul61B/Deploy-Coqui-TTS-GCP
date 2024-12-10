from helpers.tts import text_to_speech
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn


app = FastAPI()


@app.post("/synthesize")
async def synthesize(text: str, dest: str):
    """
    Synthesize speech from text and return the audio file.
    """
    file_path = text_to_speech(text, file_path=dest)
    return FileResponse(file_path, media_type="audio/wav", filename=file_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
