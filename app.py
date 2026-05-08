import streamlit as st
from PIL import Image

from synthscope.detector import analyze_image
from synthscope.metadata import analyze_metadata


st.title("SynthScope - AI Image Inspector")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption=uploaded_file.name)

    metadata = analyze_metadata(image, uploaded_file)
    file_size = (
        f"{metadata['file_size_kb']} KB"
        if metadata["file_size_kb"] is not None
        else "Unknown"
    )

    st.subheader("Metadata Analysis")
    st.table(
        [
            {"Field": "File name", "Value": metadata["file_name"]},
            {"Field": "File size", "Value": file_size},
            {"Field": "Image format", "Value": metadata["image_format"]},
            {"Field": "Width", "Value": f"{metadata['width']} px"},
            {"Field": "Height", "Value": f"{metadata['height']} px"},
            {"Field": "Has EXIF", "Value": "Yes" if metadata["has_exif"] else "No"},
            {"Field": "EXIF fields count", "Value": metadata["exif_fields_count"]},
            {"Field": "Software", "Value": metadata["software"] or "Not found"},
            {"Field": "Camera make", "Value": metadata["camera_make"] or "Not found"},
            {"Field": "Camera model", "Value": metadata["camera_model"] or "Not found"},
        ]
    )

    for warning in metadata["warning_messages"]:
        st.warning(warning)

    result = analyze_image(image)

    st.subheader("AI Detection")
    st.metric("AI probability", f"{result['ai_probability']:.1%}")
    st.write("Risk level:", result["risk_level"])

    st.write("Explanation:")
    for item in result["explanation"]:
        st.write(f"- {item}")

    st.caption("This result is experimental and should not be used as definitive proof.")
