from PIL import Image, ImageDraw
from glob import glob
from ntpath import basename
from copy import deepcopy
from . import image_to_bytes

images = {}

for img in glob('cogs/images/expanding_brain/*.jpg'):
    name = basename(img)
    images[name[:-4]] = Image.open(img).convert('RGBA')

def _get_right_list(l: int):
    if l == 2:
        return (
            (50, 50),
            (50, 300)
        )
    elif l == 3:
        return (
            (50, 50),
            (50, 300),
            (50, 550)
        )
    elif l == 4:
        return (
            (50, 50),
            (50, 350),
            (50, 700),
            (50, 900)
        )
    elif l == 5:
        return (
            (50, 50),
            (50, 350),
            (50, 550),
            (50, 700),
            (50, 950)
        )
    elif l == 6:
        return (
            (50, 50),
            (50, 250),
            (50, 500),
            (50, 700),
            (50, 950),
            (50, 1200)
        )
    else:
        raise IndexError()

async def make_expanding_brain(words: list, font):
    #make sure not to edit the original
    img = deepcopy(images[f'{len(words)}panels'])
    locations = _get_right_list(len(words))
    context = ImageDraw.Draw(img)
    for (locs, phrase) in zip(locations, words):
        context.text(locs, phrase, (0, 0, 0), font = font)
    return image_to_bytes(img)
