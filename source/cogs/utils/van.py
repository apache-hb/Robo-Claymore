from PIL import Image
from io import BytesIO

van_image = Image.open('cogs/images/creepy_van.png').convert('RGBA')

#this is the center of the window
window_loc = (90, 440)

async def overlay_van(avatar: BytesIO):
	avatar.seek(0)
	avatar_img = Image.open(avatar).convert('RGBA')

	avatar_img.thumbnail((135, 135), Image.ANTIALIAS)

	w, h = avatar_img.size
	x_loc = window_loc[0]#int(window_loc[0] - w // 2)
	y_loc = window_loc[1]#int(window_loc[1] - h // 2)
	ret = Image.new("RGBA", van_image.size, (255, 255, 255, 255))

	ret.paste(avatar_img, (y_loc, x_loc), avatar_img)
	ret.paste(van_image, (0, 0), van_image)

	res = BytesIO()
	ret.save(res, format = 'PNG')
	return res