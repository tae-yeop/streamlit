from math import e
import streamlit as st
from PIL import Image

import style

st.title("Pytorch Style Transfer")

img = st.sidebar.selectbox('Select image', ('amber.jpg', 'cat.png'))

style_name = st.sidebar.selectbox(
    'Select Style',
    ('candy', 'mosaic', 'rain-princess', 'undie')
)

model = "saved_models/" + style_name + ".pth"
input_image = "images/content-images/" + img
output_image = "images/output-images/" + style_name + "-" + img

# Markdown
st.write("### Source Image:")
image = Image.open(input_image)
st.image(image, width=400)

clicked = st.button("Stylize")

if clicked:
	model = style.load_model(model)
	style.stylize(model, input_image, output_image)

	st.write("### Source Image:")
	image = Image.open(output_image)
	st.image(image, width=400)
