from __future__ import annotations

from typing import Any

from PIL import ExifTags, Image


NO_EXIF_WARNING = (
    "No EXIF metadata found. This may happen for AI-generated, edited, or "
    "platform-compressed images."
)


def _get_file_size_kb(uploaded_file: Any) -> float | None:
    size = getattr(uploaded_file, "size", None)
    if size is None and hasattr(uploaded_file, "getbuffer"):
        size = len(uploaded_file.getbuffer())

    if size is None:
        return None

    return round(size / 1024, 2)


def analyze_metadata(image: Image.Image, uploaded_file: Any) -> dict[str, object]:
    """Return basic file, image, and EXIF metadata for an uploaded image."""
    warning_messages: list[str] = []

    try:
        exif_data = image.getexif()
        exif_fields = {
            ExifTags.TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()
        }
    except Exception as exc:
        exif_fields = {}
        warning_messages.append(f"Could not read EXIF metadata: {exc}")
    has_exif = bool(exif_fields)

    if not has_exif:
        warning_messages.append(NO_EXIF_WARNING)

    return {
        "file_name": getattr(uploaded_file, "name", None) or "unknown",
        "file_size_kb": _get_file_size_kb(uploaded_file),
        "image_format": image.format or "unknown",
        "width": image.width,
        "height": image.height,
        "has_exif": has_exif,
        "exif_fields_count": len(exif_fields),
        "software": exif_fields.get("Software"),
        "camera_make": exif_fields.get("Make"),
        "camera_model": exif_fields.get("Model"),
        "warning_messages": warning_messages,
    }
