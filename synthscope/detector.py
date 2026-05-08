from __future__ import annotations

from PIL import Image


def analyze_image(image: Image.Image) -> dict[str, object]:
    """Return a deterministic mock AI-detection result for an image."""
    width, height = image.size
    image_format = (image.format or "unknown").lower()
    mode = image.mode or "unknown"
    megapixels = (width * height) / 1_000_000
    aspect_ratio = max(width, height) / max(1, min(width, height))

    score = 0.25
    explanation: list[str] = []

    if megapixels >= 4:
        score += 0.18
        explanation.append("Large image dimensions can be associated with generated or upscaled content.")
    else:
        score -= 0.06
        explanation.append("Image dimensions are modest, which lowers the mock AI score.")

    if image_format in {"webp", "png"}:
        score += 0.14
        explanation.append(f"{image_format.upper()} format slightly increases the mock AI score.")
    elif image_format in {"jpg", "jpeg"}:
        score -= 0.08
        explanation.append("JPEG format slightly lowers the mock AI score in this mock detector.")
    else:
        explanation.append("Unknown image format keeps the mock format score neutral.")

    if aspect_ratio >= 2:
        score += 0.12
        explanation.append("Unusually wide or tall aspect ratio increases the mock risk score.")
    else:
        explanation.append("Aspect ratio is within a common range.")

    if "A" in mode:
        score += 0.10
        explanation.append("Alpha channel detected, which raises the mock AI score.")
    else:
        explanation.append("No alpha channel detected.")

    # Add a stable, small adjustment from image metadata to avoid many identical scores.
    signature = (width * 31 + height * 17 + sum(ord(char) for char in image_format + mode)) % 21
    score += (signature - 10) / 100

    ai_probability = min(0.98, max(0.02, score))
    real_probability = 1 - ai_probability

    if ai_probability < 0.35:
        risk_level = "Low"
    elif ai_probability < 0.65:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "ai_probability": round(ai_probability, 4),
        "real_probability": round(real_probability, 4),
        "risk_level": risk_level,
        "explanation": explanation,
    }
