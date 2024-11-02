FROM python:3.10-slim

WORKDIR /data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    fonts-dejavu-core \

RUN mkdir -p /data/input /data/output

COPY txt_to_pdf.py .

ENTRYPOINT ["python", "txt_to_pdf.py"]
