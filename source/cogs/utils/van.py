"""
This module handles the van image manip
Internal use only
"""

from io import BytesIO
from PIL import Image
from .converters import bytes_to_image, image_to_bytes

VAN_IMAGE = Image.open('images/creepy_van.png').convert('RGBA')

#this is the center of the window
WINDOW_LOC = (440, 90)

async def overlay_van(avatar: BytesIO):
    """Overlay an image onto the inside of a van"""
    avatar_img = bytes_to_image(avatar)

    avatar_img.thumbnail((135, 135), Image.ANTIALIAS)

    ret = Image.new("RGBA", VAN_IMAGE.size, (255, 255, 255, 255))

    ret.paste(avatar_img, WINDOW_LOC, avatar_img)
    ret.paste(VAN_IMAGE, (0, 0), VAN_IMAGE)

    return image_to_bytes(ret)
