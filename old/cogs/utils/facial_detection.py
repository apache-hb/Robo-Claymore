"""
Package for facial detection
"""

import io
import cv2
from .converters import bytes_to_cv2, bytes_to_image, image_to_bytes

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

    face = bytes_to_cv2(face_image)
    eye_locs = await find_eyes(face)

    #now convert the face from BytesIO to PIL.Image to do the editing
    output = bytes_to_image(face_image)

    w, h = output.size()
    #if w > 3000 or h > 3000:
    #    raise TypeError()
    #eye_image is alread a PIL.Image

    for (x, y, w, h) in eye_locs:
        wsize = (w * 2) // 1.25 #corectly size the eyes
        hsize = (h * 2) // 1.25
        simage = eye_image.resize((int(wsize), int(hsize)))

        output.paste(simage, (int(x - (w/4)), int(y - (h/4))), simage)

    return image_to_bytes(output)
