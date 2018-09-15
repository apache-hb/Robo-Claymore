"""
Common network requests
safe for external use
"""

from io import BytesIO
from mimetypes import MimeTypes
import aiohttp
from discord import Embed
from .shortcuts import quick_embed
from urllib.parse import urlencode
#import hastebin.async_hastebin as __hastebin
import json

MIME = MimeTypes()

TINYURL_URL = 'http://tinyurl.com/api-create.php?url='

async def tinyurl(url: str) -> str:
    """shorten a url with tinyurl.com"""
    async with aiohttp.ClientSession() as session:
        async with session.get(TINYURL_URL + url, timeout=10) as resp:
            return await resp.text()

HASTEBIN_URL = 'https://hastebin.com/documents'
GITHUB_URL = 'https://api.github.com'

async def gist(content: str, key: str) -> str:
    headers = { 'Authorization': f'token {key}' }
    params = { 'scope': 'gist' }
    payload = { 
        'description': 'GIST created by RoboClaymore#0757',
        'public': True,
        'files': {
            'RoboClaymore#0757 gist': {
                'content': content
            }
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            GITHUB_URL + '/gists',
            headers = headers,
            params = params,
            data = json.dumps(payload)
        ) as resp:
            print(await resp.text())
            ret = json.loads(await resp.text())
            return ret['url']

#this code is taken directly from https://github.com/LyricLy/hastebin.py/blob/master/hastebin/async_hastebin.py
#its apparently part of hastebin.py
#but guess what
#the __init__.py file doesnt import it, so you cant use it without making it completley non portable
#nice one
async def __post(content):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://hastebin.com/documents",data=content.encode('utf-8')) as post:
            post = await post.json()
            return "https://hastebin.com/{}".format(post['key'])

async def hastebin(content: str) -> str:
    """upload content to hastebin.com"""
    return await __post(content)

async def hastebin_error(ctx, content: str) -> Embed:
    """upload something to hastebin and return an embed to send to chat"""
    embed = quick_embed(
        ctx,
        title = 'Too much text for me to send at once',
        description = 'But do not fear'
    )
    embed.add_field(name = 'I have put it on hastebin for you', value = await hastebin(content))
    return embed

async def to_file(content: str, name: str = 'file') -> BytesIO:
    f = discord.File(io.BytesIO(bytes(ret, 'ascii')).getvalue(), filename = f'{name}.txt')
    return f

async def exists(url: str) -> bool:
    """check if a url is live and is valid"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return int(await resp.status()) < 400

async def url_request(**kwargs) -> str:
    """request the raw text from a url"""
    async with aiohttp.ClientSession() as session:
        async with session.get(**kwargs) as resp:
            return await resp.text()

async def json_request(url: str):
    """request a json resonse from a url"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def request_async(**kwargs):
    """request a url from the web"""
    async with aiohttp.ClientSession() as session:
        async with session.get(**kwargs) as resp:
            return resp

async def get_bytes(url: str) -> BytesIO:
    """Get the bytesio from a weburl, handy for downloading images"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return BytesIO(await resp.read())

#get the last image put in chat
async def get_image(ctx) -> str:
    """Get the last image put into a discord chat"""
    if ctx.message.attachments:
        return ctx.message.attachments[0].url
    channel = ctx.message.channel
    async for message in channel.history(limit=25):
        if message.attachments:
            return message.attachments[0].url
