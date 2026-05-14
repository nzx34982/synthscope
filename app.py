import csv
from io import StringIO

import streamlit as st
from PIL import Image

from synthscope.detector import analyze_image
from synthscope.metadata import analyze_metadata


def analyze_batch_file(uploaded_file):
    """Analyze one uploaded file and return one table row."""
    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)

        metadata = analyze_metadata(image, uploaded_file)
        result = analyze_image(image)

        return {
            "file_name": metadata["file_name"],
            "image_format": metadata["image_format"],
            "width": metadata["width"],
            "height": metadata["height"],
            "ai_probability": f"{result['ai_probability']:.4f}",
            "real_probability": f"{result['real_probability']:.4f}",
            "risk_level": result["risk_level"],
            "has_exif": metadata["has_exif"],
            "exif_fields_count": metadata["exif_fields_count"],
            "software": metadata["software"] or "",
            "error": "",
        }
    except Exception as exc:
        return {
            "file_name": getattr(uploaded_file, "name", "unknown"),
            "image_format": "",
            "width": "",
            "height": "",
            "ai_probability": "",
            "real_probability": "",
            "risk_level": "",
            "has_exif": "",
            "exif_fields_count": "",
            "software": "",
            "error": str(exc),
        }


def rows_to_csv(rows):
    """Convert batch analysis rows to CSV text."""
    if not rows:
        return ""

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


st.title("SynthScope - AI Image Inspector")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "webp"],
    key="single_upload",
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

st.divider()
st.subheader("Batch Analysis")

batch_files = st.file_uploader(
    "Upload multiple images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
    key="batch_upload",
)

if batch_files:
    batch_rows = [analyze_batch_file(file) for file in batch_files]

    st.dataframe(batch_rows, use_container_width=True)

    csv_report = rows_to_csv(batch_rows)
    st.download_button(
        "Download CSV report",
        data=csv_report,
        file_name="synthscope_batch_report.csv",
        mime="text/csv",
    )
