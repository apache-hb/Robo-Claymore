import io
import cv2
import numpy as np

from PIL import Image, ImageDraw

eye_cascade = cv2.CascadeClassifier('cogs/cascades/eye_cascade.xml')

async def find_eyes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    try: #do this to silence warnings
        eyes[0]
    except IndexError:
        raise LookupError("No eyes were found")

    return eyes

async def replace_eyes(face_image: io.BytesIO, eye_image):

    face_image.seek(0)
    file_bytes = np.asarray(bytearray(face_image.read()), dtype = np.uint8)
    #convert BytesIO to cv2.image to find the eyes
    face = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    eye_locs = await find_eyes(face)

    #now convert the face from BytesIO to PIL.Image to do the editing
    face_image.seek(0)
    output = Image.open(face_image).convert('RGBA')
    #eye_image is alread a PIL.Image

    for (x, y, w, h) in eye_locs:
        wsize = (w * 2) // 1.25
        hsize = (h * 2) // 1.25
        simage = eye_image.resize((int(wsize), int(hsize)))

        output.paste(simage, (int(x - (w/4)), int(y - (h/4))), simage)

    ret = io.BytesIO()
    output.save(ret, format = 'PNG')
    return ret
