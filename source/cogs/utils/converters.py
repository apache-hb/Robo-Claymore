from PIL import Image
from io import BytesIO
import cv2
import numpy as np

def bytes_to_image(image: BytesIO) -> Image:
	image.seek(0)
	return Image.open(image).convert('RGBA')

def image_to_bytes(image: Image) -> BytesIO:
	ret = BytesIO()
	image.save(ret, format = 'PNG')
	return ret

def bytes_to_cv2(image: BytesIO):
	image.seek(0)
	image_bytes = np.asarray(bytearray(image.read()), dtype = np.uint8)
	return cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
