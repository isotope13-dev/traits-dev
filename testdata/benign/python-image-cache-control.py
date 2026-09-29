"""Fetch and cache a real preview image for a local gallery."""

from urllib.request import urlopen
from PIL import Image
from io import BytesIO

PREVIEW = "https://images.example.org/gallery/preview.webp?size=small"
def load_preview():
    with urlopen(PREVIEW) as response:
        return Image.open(BytesIO(response.read())).convert("RGB")
