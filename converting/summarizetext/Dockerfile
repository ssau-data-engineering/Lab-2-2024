FROM python:3.9-slim

WORKDIR /data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY text_to_conspect.py .

ENTRYPOINT ["python", "text_to_conspect.py"]