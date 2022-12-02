import streamlit as st
from PIL import Image
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from torch import autocast
from rembg import remove

st.text('Version : 1.0 ')

device = "cuda"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "lambdalabs/sd-pokemon-diffusers",
    local_files_only=True,
    torch_dtype=torch.float16
)
pipe = pipe.to(device)


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


st.header("Turn your image into Pokémon")
st.write("Choose any image and get corresponding Pokémon art:")

uploaded_file = st.file_uploader("Choose an image...")


def imgGen2(img1,vprompt,value):
    init_image = img1.convert("RGB")
    init_image = init_image.resize((512, 512))  # proper cropping may be required

    init_image_nobg = remove(init_image).convert("RGB")
    prompt = vprompt
    scale = 2
    n_samples = 4

    # Sometimes the nsfw checker is confused by the Pokémon images, you can disable
    # it at your own risk here

    def null_safety(images, **kwargs):
        return images, False

    pipe.safety_checker = null_safety
    with autocast("cuda"):

        images = pipe(
            n_samples * [prompt],
            init_image=init_image_nobg,
            strength=value,
            guidance_scale=scale,
        ).images

    grid = image_grid(images, rows=2, cols=2)

    return grid

caption = st.text_input('Prompt', "super cool electric fire rock Pokémon")
values = st.slider(
    'Power of IA',
    0.0, 1.0,0.53)
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(uploaded_file, caption="Input Image", use_column_width=True)
    im = imgGen2(image,caption,values)
    st.image(im, caption="Pokémon art", use_column_width=True)
