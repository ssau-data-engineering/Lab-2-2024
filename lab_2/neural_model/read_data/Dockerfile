FROM python:3.9-slim

RUN pip install --no-cache-dir scikit-learn

WORKDIR /app

COPY read_data.py .

RUN mkdir -p /data/input /data/output

ENTRYPOINT ["python", "read_data.py"]