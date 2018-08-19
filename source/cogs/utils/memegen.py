from PIL import Image, ImageDraw
from .facial_detection import bytes_to_image, image_to_bytes
from io import BytesIO

def make_meme(image: BytesIO, font, header: str = 'top text', footer: str = 'bottom text'):
	img = bytes_to_image(image)
	w, h = img.size
	#give the image white bars above and below
	template = Image.new('RGBA', (w, int(h * 1.3)), (255, 255, 255, 255))
	template.paste(
		img,
		(0, int((h)//6))
	)

	context = ImageDraw.Draw(template)

	hw, _ = context.textsize(header, font = font)
	#draw header
	context.text((int((w-hw)//2), 25), header, (0, 0, 0), font = font)

	fw, _ = context.textsize(footer, font = font)

	#draw footer
	context.text(((w-hw)//2, int(h * 1.15)), footer, (0, 0, 0), font = font)

	return image_to_bytes(template)