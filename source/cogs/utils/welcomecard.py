from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .converters import bytes_to_image, image_to_bytes
from glob import glob
import discord
from copy import copy
from . import get_bytes
from ntpath import basename


CARDS = {}

font = ImageFont.truetype('cogs/fonts/papers_please.ttf', size = 155)

def clean_name(name: str):
    while not name.endswith('.'):
        name = name[:-1]

    return name[:-1]

for card in glob('images/welcome_cards/*.*'):
    CARDS[clean_name(basename(card))] = Image.open(card).convert('RGBA')

async def card_choices():
    return CARDS.keys()

async def get_card(name: str):
    return CARDS[name]

#TODO finish this
async def make_card(card: str, usr: discord.Member, side_text: str, bottom_text: str):
    img = copy(CARDS[card])
    avatar = bytes_to_image(await get_bytes(usr.avatar_url))

    avatar = avatar.resize((512, 512), Image.ANTIALIAS)

    img.paste(avatar, (256, 256), avatar)

    draw = ImageDraw.Draw(img)

    draw.text((0, 0), 'name jeff', (0, 0, 0), font = font)

    return image_to_bytes(img)
    
