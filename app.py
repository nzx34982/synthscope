import streamlit as st
from PIL import Image


st.title("SynthScope - AI Image Inspector")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption=uploaded_file.name)

    st.write("File name:", uploaded_file.name)
    st.write("Image format:", image.format)
    st.write("Size:", f"{image.width} x {image.height} px")
