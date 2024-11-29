FROM python:3.9

ENV TZ=Europe/Berlin

RUN apt-get update && \
   apt-get install -y ffmpeg && \
   apt-get clean && \
   rm -rf /var/lib/apt/lists/*

WORKDIR /data

COPY requirements.txt /data/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /data

CMD ["bash"]