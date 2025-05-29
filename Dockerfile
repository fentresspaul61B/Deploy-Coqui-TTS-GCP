# # Use an official Python runtime as a parent image
# # FROM python:3.10
# FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

# # Set the working directory in the container
# WORKDIR /app

# ENV COQUI_TOS_AGREED=1

# # Copy the requirements file into the container
# COPY requirements.txt .

# # Install the required packages
# RUN pip install --no-cache-dir -r requirements.txt

# # Install ffmpeg
# # RUN apt-get update && \
# #     apt-get install -y ffmpeg && \
# #     apt-get clean && \
# #     rm -rf /var/lib/apt/lists/*

# # RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
# #     | tar -xJ && \
# #     cp ffmpeg-*-amd64-static/{ffmpeg,ffprobe} /usr/local/bin/ && \
# #     chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
# #     rm -rf ffmpeg-*-amd64-static


# RUN python -c "from TTS.api import TTS; tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')"

# # RUN ls -R /root/.local/share/tts

# # Copy the application code into the container
# COPY main.py .
# COPY helpers ./helpers

# # Expose port 8080
# EXPOSE 8080

# # Command to run the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]



# ──────────────────────────────────────────────────────────────
# Base image
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

WORKDIR /app
ENV COQUI_TOS_AGREED=1

# ──────────────────────────────────────────────────────────────
# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txts

# ──────────────────────────────────────────────────────────────
# ► STATIC FFMPEG ◄
# 1. Copy the exact tarball into the image
#    (make sure the file sits next to your Dockerfile, or adjust the path)
COPY ffmpeg-git-amd64-static.tar.xz /tmp/

# 2. Unpack, move the two binaries we need, and wipe the leftovers
RUN tar -xJf /tmp/ffmpeg-git-amd64-static.tar.xz -C /tmp && \
    cp /tmp/ffmpeg-*/ffmpeg  /usr/local/bin/ && \
    cp /tmp/ffmpeg-*/ffprobe /usr/local/bin/ && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    rm -rf /tmp/ffmpeg-git-amd64-static.tar.xz /tmp/ffmpeg-*


# ──────────────────────────────────────────────────────────────
# Pre-download the TTS model (optional but keeps first request fast)
RUN python -c "from TTS.api import TTS; tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')"


# ──────────────────────────────────────────────────────────────
# App code
COPY main.py .
COPY helpers ./helpers

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
