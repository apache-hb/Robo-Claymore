import json

import sys
import os

import discord

#for embed checking
from urllib.request import pathname2url
from mimetypes import MimeTypes

#keep this file as minimal as possible

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
import asyncio
import async_timeout
from bs4 import BeautifulSoup
session = aiohttp.ClientSession()

async def shorten_url(long_url: str):
    url = "http://tinyurl.com/create.php?source=indexpage&url=" + long_url + "&submit=Make+TinyURL%21&alias="
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            if "The custom alias" in soup.p.b.string:
                return "url machine broke"
            else:
                return soup.find_all('div', {'class': 'indent'})[1].b.string


mime = MimeTypes()
def is_embedable(url: str):
    url = pathname2url(url)
    mime_type = mime.guess_type(url)
    return mime_type[0] in ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']
