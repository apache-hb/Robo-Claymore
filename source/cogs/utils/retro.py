import aiohttp
import re
from ..store import url_request

retro_url = 'https://photofunia.com/effects/retro-wave?server=3'

retro_regex = re.compile("((https)(\:\/\/|)?u3\.photofunia\.com\/.\/results\/.\/.\/.*(\.jpg\?download))")

async def make_retro(text, kind):
    if '|' in text:
        text = text.split('|')
    elif len(text) >= 15:#split into 15 char bits
        text = [text[i:i + 15] for i in range(0, len(text), 15)]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'
    }
    payload = aiohttp.FormData()
    payload.add_field('current-category', 'all_effects')
    payload.add_field('bcg', kind)
    payload.add_field('txt', '4')

    for (idx, line) in enumerate(text[:3], start = 1):
        payload.add_field('text' + str(idx), line.replace("'", "\'"))

    async with aiohttp.ClientSession() as session:
        async with session.post(
                retro_url,
                data = payload,
                headers = headers,
                timeout = aiohttp.ClientTimeout(total = 7)
            ) as resp:
            txt = await resp.text()

    match = retro_regex.findall(txt)
    if match:
        return match[0][0]
    return
