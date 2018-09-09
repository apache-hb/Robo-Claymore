from PIL import Image, ImageFilter
from PIL.ImageEnhance import Color
from .converters import image_to_bytes
import io

async def do_deepfry(img: Image):
    converter = Color(img)
    ret = converter.enhance(10)
    return image_to_bytes(ret)

async def jpegify(img: Image):
    ret = io.BytesIO()
    img.convert('RGB').save(ret, format = 'JPEG', quality = 1)
    return ret

async def do_sharpen(img: Image):
    sharp = img.filter(ImageFilter.SHARPEN)
    return image_to_bytes(sharp)

async def emboss(img: Image):
    embossed = img.filter(ImageFilter.EMBOSS)
    ret = Image.blend(img, embossed, 0.8)
    return image_to_bytes(ret)