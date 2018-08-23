from PIL import Image, ImageDraw, ImageFont
from copy import deepcopy, copy
from . import image_to_bytes
from glob import glob
from ntpath import basename

blue_button_loc = (100, 100)
button_choice_locs = ((50, 100), (50, 200))
class_note_loc = (100, 100)
door_kick_loc = (100, 100)
first_words_loc = (100, 100)
letter_loc = (100, 100)
prison_loc = (100, 100)
retarded_loc = (100, 100)
shouting_locs = ((50, 50), (200, 50))
tweet_loc = (50, 50)
villan_locs = ((50, 50), (50, 200))

images = {}
files = glob('cogs/images/*.jpg')
files.extend(glob('cogs/images/*.png'))

for each in files:
	name = basename(each)
	images[name[:-4]] = Image.open(each).convert('RGBA')

font = ImageFont.truetype('cogs/fonts/comic_sans.ttf', size = 35)

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
	pass

async def do_prison(text: str):
	pass

small_font = ImageFont.truetype('cogs/fonts/comic_sans.ttf', size = 25)

async def do_retard(text: str):
	img = copy(images['retarded'])
	draw = ImageDraw.Draw(img)
	draw.text((400, 50), text, (0, 0, 0), font = small_font)
	return image_to_bytes(img)

async def do_shout(first: Image, second: Image):
	pass

async def do_tweet(text: str):
	pass

async def do_villan_image(first: Image, second: Image):
	img = copy(images['villans'])
	first.thumbnail((512, 512), Image.ANTIALIAS)
	second.thumbnail((512, 512), Image.ANTIALIAS)
	img.paste(first, (200, 100), first)
	img.paste(second, (200, 1300), second)
	return image_to_bytes(img)