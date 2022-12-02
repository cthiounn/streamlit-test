# syntax = docker/dockerfile:1.2
FROM python:3.10

WORKDIR /root/.u2net/
RUN --mount=type=cache,target=/var/cache/ curl -SL  https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o u2net.onnx


WORKDIR /
RUN --mount=type=cache,target=/var/cache/ curl -SL https://minio.lab.sspcloud.fr/cthiounn2/diffuser-pokemon.tar.gz -o diffuser-pokemon.tar.gz 
RUN tar -xvf diffuser-pokemon.tar.gz --strip-components=2 -C /root/ && rm diffuser-pokemon.tar.gz  
#&& cp -rf /root/home/onyxia/.cache/* /root/.cache && rm -rf /root/home/onyxia/.cache/*
# Creation of a working directory app

COPY requirements.txt /tmp/
RUN --mount=type=cache,target=/var/cache/pip pip install --requirement /tmp/requirements.txt

WORKDIR /app
# Copy all the files of this project inside the container
COPY . .

CMD ["streamlit", "run", "myapp.py","--server.port", "3838"]