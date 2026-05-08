import streamlit as st
from PIL import Image

from synthscope.detector import analyze_image


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

    result = analyze_image(image)

    st.subheader("AI Detection")
    st.metric("AI probability", f"{result['ai_probability']:.1%}")
    st.write("Risk level:", result["risk_level"])

    st.write("Explanation:")
    for item in result["explanation"]:
        st.write(f"- {item}")

    st.caption("This result is experimental and should not be used as definitive proof.")
