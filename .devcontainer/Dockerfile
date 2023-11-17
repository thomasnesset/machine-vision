FROM debian:stable

RUN apt-get update && apt-get install -y \
    libgl1 \
    python3 \
    python3-pil \
    python3-pil.imagetk \
    python3-tk \
    python3-pip

RUN pip install --break-system-packages face-recognition numpy opencv-python
