import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from torch import autocast
import requests
from io import BytesIO
from rembg import remove


device = "gpu"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "lambdalabs/sd-pokemon-diffusers", torch_dtype=torch.float16
)
pipe = pipe.to(device)


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


st.header("Turn your image into Pokémon")
st.write("Choose any image and get corresponding Pokémon art:")

uploaded_file = st.file_uploader("Choose an image...")


def imgGen2(img1):
    init_image = img1.convert("RGB")
    width, height = init_image.size
    init_image = init_image.resize((512, 512))  # proper cropping may be required

    init_image_nobg = remove(init_image).convert("RGB")
    prompt = "super cool electric fire rock Pokémon"
    scale = 2
    n_samples = 4

    # Sometimes the nsfw checker is confused by the Pokémon images, you can disable
    # it at your own risk here

    def null_safety(images, **kwargs):
        return images, False

    pipe.safety_checker = null_safety

    images = pipe(
        n_samples * [prompt],
        init_image=init_image_nobg,
        strength=0.53,
        guidance_scale=scale,
    ).images

    grid = image_grid(images, rows=2, cols=2)

    return grid


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(uploaded_file, caption="Input Image", use_column_width=True)
    im = imgGen2(image)
    st.image(im, caption="Pokémon art", use_column_width=True)
