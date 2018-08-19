import aiohttp
from mimetypes import MimeTypes
from urllib.request import pathname2url
from io import BytesIO
import json
import discord

MIME = MimeTypes()

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

async def url_request(**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(**kwargs) as resp:
            return await resp.text()

async def json_request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def request_async(**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(**kwargs) as resp:
            return resp

async def get_bytes(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return BytesIO(await resp.read())

#get the last image put in chat
async def get_image(ctx):
    channel = ctx.message.channel
    async for message in channel.history(limit = 25):
        if message.attachments:
            return message.attachments[0].url