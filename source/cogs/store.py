import json

import sys
import os

import discord

#for embed checking
from urllib.request import pathname2url
from mimetypes import MimeTypes

#keep this file as minimal as possible

dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))

def style_embed(ctx, title: str, description: str='', color: int=None):
    if color is None:
        try: color = ctx.guild.me.color
        except AttributeError: color = Store.default_color
    embed=discord.Embed(title=title, description=description,color=color)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    return embed


def pyout(message: str):
    if not Store.silent:
        print(message)
    return Store.silent

def qlog(message: str):
    f = open('cogs/store/direct.log', 'a')
    f.write(message)
    f.close()

def add_guild(guild):
    pass

class Store:

    total_messages = 0

    current_system = ''

    silent = False

    default_color = 0xe00b3c

    frames = []

    config = json.load(open('cogs/store/config.json'))

    whitelist = json.load(open('cogs/store/whitelist.json'))

    blacklist = json.load(open('cogs/store/blacklist.json'))

if Store.current_system == 'mac':
    sys.path.append('/usr/local/lib/python3.6/site-packages')

#for url shortening
import aiohttp

async def shorten_url(long_url: str):
    url = "http://tinyurl.com/api-create.php?url=" + long_url
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            return await response.text()

mime = MimeTypes()
def is_embedable(url: str):
    url = pathname2url(url)
    mime_type = mime.guess_type(url)
    return mime_type[0] in ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']
