from tts import text_to_speech
from fastapi import FastAPI
from fastapi.responses import FileResponse
# from fastapi.responses import StreamingResponse
import uvicorn
# from io import BytesIO


app = FastAPI()


@app.post("/synthesize")
async def synthesize(text: str):
    """
    Synthesize speech from text and return the audio file.
    """
    file_path = text_to_speech(text)
    return FileResponse(file_path, media_type="audio/wav", filename=file_path)

# @app.post("/synthesize")
# async def synthesize(text: str):
#     """
#     Synthesize speech from text and return the audio file.
#     """
#     file_path = text_to_speech(text)
#     # return FileResponse(
#           file_path, media_type="audio/wav", filename="output.wav")
#     return StreamingResponse(
#           BytesIO(audio_data), media_type="audio/wav", headers={
#         "Content-Disposition": "attachment; filename=output.wav"
#     })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
