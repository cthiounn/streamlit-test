import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np


st.header("Turn your image into Pokémon")
st.write("Choose any image and get corresponding Pokémon art:")

uploaded_file = st.file_uploader("Choose an image...")

def imgGen2(img1):
    return img1


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(uploaded_file, caption="Input Image", use_column_width=True)
    im = imgGen2(uploaded_file)
    st.image(im, caption="Pokémon art", use_column_width=True)
