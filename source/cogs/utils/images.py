"""
Helper commands for the images cog
Not safe for external use
"""

from copy import copy, deepcopy
from glob import glob
from ntpath import basename
from PIL import Image, ImageDraw, ImageFont
from _io import BytesIO
from . import image_to_bytes

IMAGES = {}
FILES = glob('cogs/images/*.jpg')
FILES.extend(glob('cogs/images/*.png'))

for each in FILES:
    name = basename(each)
    IMAGES[name[:-4]] = Image.open(each).convert('RGBA')

font = ImageFont.truetype('cogs/fonts/comic_sans.ttf', size = 35)
small_font = ImageFont.truetype('cogs/fonts/comic_sans.ttf', size = 25)
big_font = ImageFont.truetype('cogs/fonts/comic_sans.ttf', size = 55)

async def do_choice(first: str, second: str) -> BytesIO:
    """make a choice meme"""
    img = deepcopy(IMAGES['choice'])
    draw = ImageDraw.Draw(img)
    draw.text((100, 100), first, (0, 0, 0), font = font)
    draw.text((300, 50), second, (0, 0, 0), font = font)
    return image_to_bytes(img)

async def do_button(text: str) -> BytesIO:
    """make a button hitting meme"""
    img = copy(IMAGES['button'])
    draw = ImageDraw.Draw(img)
    draw.text((50, 250), text, (0, 0, 0), font = font)
    return image_to_bytes(img)

async def do_note(text: str) -> BytesIO:
    """make a class note meme"""
    img = copy(IMAGES['class_note'])
    draw = ImageDraw.Draw(img)
    draw.text((350, 500), text, (0, 0, 0), font = font)
    return image_to_bytes(img)

async def do_kick(image: Image) -> BytesIO:
    """make a door kicking meme"""
    img = copy(IMAGES['door_kick'])
    ret = Image.new('RGBA', img.size, (255, 255, 255, 255))
    image.thumbnail((256, 256), Image.ANTIALIAS)
    ret.paste(image, (350, 50), image)
    ret.paste(img, (0, 0), img)
    return image_to_bytes(ret)

async def do_words(text: str) -> BytesIO:
    """make a meme with a baby's first words"""
    img = copy(IMAGES['first_words'])
    draw = ImageDraw.Draw(img)
    draw.text((50, 300), text, (0, 0, 0), font = font)
    return image_to_bytes(img)

async def do_prison(text: str) -> BytesIO:
    """make a prison meme"""
    img = copy(IMAGES['prison'])
    draw = ImageDraw.Draw(img)
    draw.text((250, 250), text, (0, 0, 0), font = small_font)
    return image_to_bytes(img)

async def do_retard(text: str) -> BytesIO:
    """make a retard meme"""
    img = copy(IMAGES['retarded'])
    draw = ImageDraw.Draw(img)
    draw.text((400, 50), text, (0, 0, 0), font = small_font)
    return image_to_bytes(img)

async def do_shout(first: Image, second: Image) -> BytesIO:
    """make a shouting meme"""
    img = copy(IMAGES['shouting'])
    ret = Image.new('RGBA', img.size, (255, 255, 255, 255))
    first.thumbnail((128, 128), Image.ANTIALIAS)
    second.thumbnail((128, 128), Image.ANTIALIAS)
    ret.paste(first, (30, 50), first)
    ret.paste(second, (330, 50), second)
    ret.paste(img, (0, 0), img)
    return image_to_bytes(ret)

async def do_tweet(text: str) -> BytesIO:
    """make a trump tweet meme"""
    img = copy(IMAGES['trump_tweet'])
    ret = ImageDraw.Draw(img)
    ret.text((200, 250), text, (0, 0, 0), font=BIG_FONT)
    return image_to_bytes(img)

async def do_villan_image(first: Image, second: Image) -> BytesIO:
    """make a villan meme"""
    img = copy(IMAGES['villans'])
    first.thumbnail((512, 512), Image.ANTIALIAS)
    second.thumbnail((512, 512), Image.ANTIALIAS)
    img.paste(first, (200, 100), first)
    img.paste(second, (200, 1300), second)
    return image_to_bytes(img)

async def do_rtx(first: Image, second: Image) -> BytesIO:
    """make an RTX meme"""
    img = copy(IMAGES['rtx'])
    first.thumbnail((353, 353), Image.ANTIALIAS)
    second.thumbnail((353, 353), Image.ANTIALIAS)
    ret = Image.new('RGBA', img.size, (255, 255, 255, 255))
    ret.paste(first, (0, 0), first)
    ret.paste(second, (0, 353), second)
    ret.paste(img, (0, 0), img)
    return image_to_bytes(ret)

async def do_wack(image: Image) -> BytesIO:
    """make a wack meme"""
    img = copy(IMAGES['wack'])
    w, h = img.size
    ret = Image.new('RGBA', (w, h*2), (255, 255, 255, 255))
    image.thumbnail((w, h), Image.ANTIALIAS)
    ret.paste(image, (0, 0), image)
    ret.paste(img, (0, h), img)
    return image_to_bytes(ret)

async def do_crusade(image: Image) -> BytesIO:
    """we need another crusade"""
    img = copy(IMAGES['crusade'])
    image.thumbnail((225, 225), Image.ANTIALIAS)
    img.paste(image, (0, 0), image)
    return image_to_bytes(img)

PAPERS_PLEASE = ImageFont.truetype('cogs/fonts/papers_please.ttf', size = 18)

async def do_violation(text: str) -> BytesIO:
    """Protocol violation: unfunny meme"""
    img = copy(IMAGES['unfunnymeme'])
    ret = ImageDraw.Draw(img)
    ret.text((25, 55), text, (101, 95, 85), font = PAPERS_PLEASE)
    return image_to_bytes(img)
