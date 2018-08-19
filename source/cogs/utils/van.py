from PIL import Image
from io import BytesIO
from . import image_to_bytes, bytes_to_image

van_image = Image.open('cogs/images/creepy_van.png').convert('RGBA')

#this is the center of the window
window_loc = (440, 90)

async def overlay_van(avatar: BytesIO):
    avatar_img = bytes_to_image(avatar)

    avatar_img.thumbnail((135, 135), Image.ANTIALIAS)

    ret = Image.new("RGBA", van_image.size, (255, 255, 255, 255))

    ret.paste(avatar_img, window_loc, avatar_img)
    ret.paste(van_image, (0, 0), van_image)

    return image_to_bytes(ret)
