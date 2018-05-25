import json
import discord
import aiohttp
from urllib.request import pathname2url
from mimetypes import MimeTypes
from emoji import UNICODE_EMOJI as uemoji

MIME = MimeTypes()

def quick_embed(ctx, title: str, description: str = None, colour: int = 0x023cfc):
    try: colour = ctx.me.colour
    except AttributeError: pass
    return discord.Embed(title = title, description = description, colour = colour)

async def tinyurl(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://tinyurl.com/api-create.php?url=' + url, timeout=10) as resp:
            return await resp.text()

async def hastebin(content: str):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://hastebin.com/documents', data = content.encode('utf-8')) as post:
            post = await post.json()
            return 'https://hastebin.com/' + post['key']

async def hastebin_error(ctx, content: str):
    embed = quick_embed(ctx, title = 'Too much text for me to send at once', description = 'But do not fear')
    embed.add_field(name = 'I have put it on hastebin for you', value = await hastebin(content))
    return embed

async def exists(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return int(await resp.status()) < 400

def embedable(url: str):
    url = pathname2url(url)
    mime_type = MIME.guess_type(url)
    return mime_type[0] in ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']

def emoji(emoji: str):
    #if the string is surrounded with <> there is a chance its a discord emoji
    if emoji.startswith('<') and emoji.endswith('>') and emoji.count(':') == 2:
        emoji = emoji[3:] if emoji.startswith('<a:') else emoji[2:]
        while not emoji.startswith(':'):
            emoji = emoji[1:]
        emoji = emoji[1:-1]
        if len(emoji):
            return True
        return False
    elif emoji in uemoji:
        return True
    return False

config = json.load(open('cogs/store/config.json'))

whitelist = json.load(open('cogs/store/whitelist.json'))

blacklist = json.load(open('cogs/store/blacklist.json'))

# stolen from appuselfbot
# https://github.com/appu1232/Discord-Selfbot
emoji_dict = {
    'a': ['🇦 ', '🅰', '🍙', '🔼', '4⃣'],
    'b': ['🇧 ', '🅱', '8⃣'],
    'c': ['🇨 ', '©', '🗜'],
    'd': ['🇩 ', '↩'],
    'e': ['🇪 ', '3⃣', '📧', '💶'],
    'f': ['🇫 ', '🎏'],
    'g': ['🇬 ', '🗜', '6⃣', '9⃣', '⛽'],
    'h': ['🇭 ', '♓'],
    'i': ['🇮 ', 'ℹ', '🚹', '1⃣'],
    'j': ['🇯 ', '🗾'],
    'k': ['🇰 ', '🎋'],
    'l': ['🇱 ', '1⃣', '🇮', '👢', '💷'],
    'm': ['🇲 ', 'Ⓜ', '📉'],
    'n': ['🇳 ', '♑', '🎵'],
    'o': ['🇴 ', '🅾', '0⃣', '⭕', '🔘', '⏺', '⚪', '⚫', '🔵', '🔴', '💫'],
    'p': ['🇵 ', '🅿'],
    'q': ['🇶 ', '♌'],
    'r': ['🇷 ', '®'],
    's': ['🇸 ', '💲', '5⃣', '⚡', '💰', '💵'],
    't': ['🇹 ', '✝', '➕', '🎚', '🌴', '7⃣'],
    'u': ['🇺 ', '⛎', '🐉'],
    'v': ['🇻 ', '♈', '☑'],
    'w': ['🇼 ', '〰', '📈'],
    'x': ['🇽 ', '❎', '✖', '❌', '⚒'],
    'y': ['🇾 ', '✌', '💴'],
    'z': ['🇿 ', '2⃣'],
    '0': ['0⃣ ', '🅾', '0⃣', '⭕', '🔘', '⏺', '⚪', '⚫', '🔵', '🔴', '💫'],
    '1': ['1⃣ ', '🇮'],
    '2': ['2⃣ ', '🇿'],
    '3': ['3⃣ '],
    '4': ['4⃣ '],
    '5': ['5⃣ ', '🇸', '💲', '⚡'],
    '6': ['6⃣ '],
    '7': ['7⃣ '],
    '8': ['8⃣ ', '🎱', '🇧', '🅱'],
    '9': ['9⃣ '],
    '?': ['❓ '],
    '!': ['❗ ', '❕', '⚠', '❣'],
    ' ': ['   '],
    '\n': ['\n']
}