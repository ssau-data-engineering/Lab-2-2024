FROM python:3.9-slim

WORKDIR /data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY txt_to_cons.py .

ENTRYPOINT ["python", "txt_to_cons.py"]