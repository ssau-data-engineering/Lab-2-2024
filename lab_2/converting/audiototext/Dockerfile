FROM python:3.9-slim

WORKDIR /data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY audio_to_text.py .

ENTRYPOINT ["python", "audio_to_text.py"]