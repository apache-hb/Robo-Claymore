"""
Create a `retro` image by querying an API
safe for external use
"""

import re
import aiohttp

RETRO_URL = 'https://photofunia.com/effects/retro-wave?server=3'

#stolen from notsobot
RETRO_REGEX = re.compile(
    r"((https)(\:\/\/|)?u3\.photofunia\.com\/.\/results\/.\/.\/.*(\.jpg\?download))"
)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'
}

async def make_retro(text: str, kind) -> str:
    """Make a retro image"""
    if '|' in text:
        text = text.split('|')
    elif len(text) >= 15:#split into 15 char bits
        text = [text[i:i + 15] for i in range(0, len(text), 15)]
    else:
        text = text.split(' ')

    payload = aiohttp.FormData()
    payload.add_field('current-category', 'all_effects')
    payload.add_field('bcg', kind)
    payload.add_field('txt', '4')

    for (idx, line) in enumerate(text[:3], start=1):
        payload.add_field('text' + str(idx), line.replace("'", "\'"))

    async with aiohttp.ClientSession() as session:
        async with session.post(
            RETRO_URL,
            data = payload,
            headers = HEADERS,
            timeout = aiohttp.ClientTimeout(total=7)
        ) as resp:
            txt = await resp.text()

    match = RETRO_REGEX.findall(txt)
    if match: #this bit is also stolen from notsobot
        return match[0][0]
