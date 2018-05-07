import json

import sys
import os

import discord
import time

import emoji as e
#for embed checking
from urllib.request import pathname2url
from mimetypes import MimeTypes

#keep this file as minimal as possible

dir_path = dir_path = os.path.dirname(os.path.realpath(__file__))

def reset_config():
    clean_file('./cogs/store/bot.log', 'logging file \n')
    clean_file('./cogs/store/direct.log', 'direct messages file \n')
    clean_file('./cogs/store/statistics.json', json.dumps(statistic_dict, indent=4))
    clean_file('./cogs/store/symbiosis.json', '[]')
    clean_file('./cogs/store/tags.json', '[]')
    clean_file('./cogs/store/quotes.json', '[]')
    clean_file('./cogs/store/autoreact.json', '[]')
    clean_file('./cogs/store/autorole.json', '[]')
    clean_file('./cogs/store/disabled.json', '[]')
    clean_file('./cogs/store/blacklist.json', '[]')
    clean_file('./cogs/store/blocked.json', '[]')
    clean_file('./cogs/store/whitelist.json', '[]')
    clean_file('./cogs/store/welcome.json', '[]')
    clean_file('./cogs/store/leave.json', '[]')

def is_emoji(emoji: str):
    is_anim = True if emoji.startswith('<a:') else False

    if emoji.startswith('<') and emoji.endswith('>') and emoji.count(':') == 2:
        emoji = emoji[3:] if is_anim else emoji[2:]
        while not emoji.startswith(':'):
            emoji = emoji[1:]
        emoji = emoji[1:-1]
        if len(emoji):
            return True
        return False
    elif emoji in e.UNICODE_EMOJI:
        return True
    return False

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

def guild_template(guild):
    ret = {
        "server_id": guild.id,
        "first_joined": int(time.time()),
        "contents": [

        ]
    }
    return ret

def add_guild(guild):
    #autoreact
    if not any(d['server_id'] == guild.id for d in autoreact):
        autoreact.append(guild_template(guild))
        json.dump(autoreact, open('cogs/store/autoreact.json', 'w'), indent=4)

    #autorole
    if not any(d['server_id'] == guild.id for d in autorole):
        autorole.append(guild_template(guild))
        json.dump(autorole, open('cogs/store/autorole.json', 'w'), indent=4)

    #tags
    if not any(d['server_id'] == guild.id for d in tags):
        tags.append(guild_template(guild))
        json.dump(tags, open('cogs/store/tags.json', 'w'), indent=4)

    #quotes
    if not any(d['server_id'] == guild.id for d in quotes):
        quotes.append(guild_template(guild))
        json.dump(quotes, open('cogs/store/quotes.json', 'w'), indent=4)


class Store:

    total_messages = 0

    current_system = ''

    silent = False

    default_color = 0xe00b3c

    frames = []

tags = json.load(open(dir_path + '/store/tags.json'))

quotes = json.load(open(dir_path + '/store/quotes.json'))

welcome = json.load(open(dir_path + '/store/welcome.json'))

leave = json.load(open(dir_path + '/store/leave.json'))

autoreact = json.load(open(dir_path + '/store/autoreact.json'))

autorole = json.load(open(dir_path + '/store/autorole.json'))

config = json.load(open(dir_path + '/store/config.json'))

whitelist = json.load(open(dir_path + '/store/whitelist.json'))

blacklist = json.load(open(dir_path + '/store/blacklist.json'))

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
