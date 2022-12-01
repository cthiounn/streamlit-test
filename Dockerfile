FROM python:3.10
# Creation of a working directory app
WORKDIR /app
# Copy all the files of this project inside the container
COPY . .
# Installation of code dependencies
RUN pip install -r requirements.txt
WORKDIR /root/.u2net/
ADD https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx u2net.onnx


WORKDIR /
ADD https://minio.lab.sspcloud.fr/cthiounn2/diffuser-pokemon.tar.gz diffuser-pokemon.tar.gz 
RUN tar -xvf diffuser-pokemon.tar.gz -C /root/
RUN rm diffuser-pokemon.tar.gz 
WORKDIR /app
CMD ["streamlit", "run", "myapp.py"]