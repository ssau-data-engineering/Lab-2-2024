FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s $(which ffmpeg) /usr/local/bin/ffmpeg

WORKDIR /data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY audio_to_text_.py .

ENTRYPOINT ["python", "audio_to_text_.py"]