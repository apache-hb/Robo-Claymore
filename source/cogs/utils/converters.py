"""
Converters for images to other formats
"""

import io
import cv2
import numpy as np
from PIL import Image


def bytes_to_image(image: io.BytesIO) -> Image:
    image.seek(0)
    return Image.open(image).convert('RGBA')

def image_to_bytes(image: Image) -> io.BytesIO:
    ret = io.BytesIO()
    image.save(ret, format = 'PNG')
    return ret

def bytes_to_cv2(image: io.BytesIO):
    image.seek(0)
    image_bytes = np.asarray(bytearray(image.read()), dtype = np.uint8)
    return cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
