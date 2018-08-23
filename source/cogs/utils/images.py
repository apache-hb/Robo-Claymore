from PIL import Image, ImageDraw, ImageFont
from copy import deepcopy, copy
from . import image_to_bytes
from glob import glob
from ntpath import basename

images = {}
files = glob('cogs/images/*.jpg')
files.extend(glob('cogs/images/*.png'))

for each in files:
    name = basename(each)
    images[name[:-4]] = Image.open(each).convert('RGBA')

font = ImageFont.truetype('cogs/fonts/comic_sans.ttf', size = 35)
small_font = ImageFont.truetype('cogs/fonts/comic_sans.ttf', size = 25)
big_font = ImageFont.truetype('cogs/fonts/comic_sans.ttf', size = 55)

async def do_choice(first: str, second: str):
    img = deepcopy(images['choice'])
    draw = ImageDraw.Draw(img)
    draw.text((100, 100), first, (0, 0, 0), font = font)
    draw.text((300, 50), second, (0, 0, 0), font = font)
    return image_to_bytes(img)

async def do_button(text: str):
    img = copy(images['button'])
    draw = ImageDraw.Draw(img)
    draw.text((50, 250), text, (0, 0, 0), font = font)
    return image_to_bytes(img)

async def do_note(text: str):
    img = copy(images['class_note'])
    draw = ImageDraw.Draw(img)
    draw.text((350, 500), text, (0, 0, 0), font = font)
    return image_to_bytes(img)

async def do_kick(image: Image):
    img = copy(images['door_kick'])
    ret = Image.new('RGBA', img.size, (255, 255, 255, 255))
    image.thumbnail((256, 256), Image.ANTIALIAS)
    ret.paste(image, (350, 50), image)
    ret.paste(img, (0, 0), img)
    return image_to_bytes(ret)

async def do_words(text: str):
    img = copy(images['first_words'])
    draw = ImageDraw.Draw(img)
    draw.text((50, 300), text, (0, 0, 0), font = font)
    return image_to_bytes(img)

async def do_prison(text: str):
    img = copy(images['prison'])
    draw = ImageDraw.Draw(img)
    draw.text((250, 250), text, (0, 0, 0), font = small_font)
    return image_to_bytes(img)

async def do_retard(text: str):
    img = copy(images['retarded'])
    draw = ImageDraw.Draw(img)
    draw.text((400, 50), text, (0, 0, 0), font = small_font)
    return image_to_bytes(img)

async def do_shout(first: Image, second: Image):
    img = copy(images['shouting'])
    ret = Image.new('RGBA', img.size, (255, 255, 255, 255))
    first.thumbnail((128, 128), Image.ANTIALIAS)
    second.thumbnail((128, 128), Image.ANTIALIAS)
    ret.paste(first, (30, 50), first)
    ret.paste(second, (330, 50), second)
    ret.paste(img, (0, 0), img)
    return image_to_bytes(ret)

async def do_tweet(text: str):
    img = copy(images['trump_tweet'])
    ret = ImageDraw.Draw(img)
    ret.text((200, 250), text, (0, 0, 0), font = big_font)
    return image_to_bytes(img)

async def do_villan_image(first: Image, second: Image):
    img = copy(images['villans'])
    first.thumbnail((512, 512), Image.ANTIALIAS)
    second.thumbnail((512, 512), Image.ANTIALIAS)
    img.paste(first, (200, 100), first)
    img.paste(second, (200, 1300), second)
    return image_to_bytes(img)

async def do_rtx(first: Image, second: Image):
    img = copy(images['rtx'])
    first.thumbnail((353, 353), Image.ANTIALIAS)
    second.thumbnail((353, 353), Image.ANTIALIAS)
    ret = Image.new('RGBA', img.size, (255, 255, 255, 255))
    ret.paste(first, (0, 0), first)
    ret.paste(second, (0, 353), second)
    ret.paste(img, (0, 0), img)
    return image_to_bytes(ret)

async def do_wack(image: Image):
    img = copy(images['wack'])
    w, h = img.size
    ret = Image.new('RGBA', (w, h*2), (255, 255, 255, 255))
    image.thumbnail((w, h), Image.ANTIALIAS)
    ret.paste(image, (0, 0), image)
    ret.paste(img, (0, h), img)
    return image_to_bytes(ret)
