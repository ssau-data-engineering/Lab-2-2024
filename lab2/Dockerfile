FROM python:3.11-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# # #         ffmpeg        # # #
# RUN apt-get -y update; \
#     apt-get install -y ffmpeg; \
#     rm -rf /var/lib/apt/lists/*;

# # #      requests-pdf     # # #
# RUN pip install --upgrade pip; \
#     pip install \
#     \
#     fpdf \
#     requests;

# # #          cnn          # # #
RUN pip install --upgrade pip; \
    pip install \
    \
    numpy \
    tensorflow \
    keras;