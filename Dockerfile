FROM python:3.10
# Creation of a working directory app
WORKDIR /app
# Copy all the files of this project inside the container
COPY . .
# Installation of code dependencies
RUN pip install -r requirements.txt

RUN wget https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx
WORKDIR /root/.u2net/
COPY  u2net.onnx .


WORKDIR /
RUN curl -SL https://minio.lab.sspcloud.fr/cthiounn2/diffuser-pokemon.tar.gz | tar -xvf diffuser-pokemon.tar.gz -C /
# Endpoint
CMD ["streamlit", "run", "myapp.py"]