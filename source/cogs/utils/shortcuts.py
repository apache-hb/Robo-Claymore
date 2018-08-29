"""
This module stores shortcuts for commonly performed actions
can be used externally
"""

from mimetypes import MimeTypes
from urllib.request import pathname2url
import discord
from emoji import UNICODE_EMOJI as uemoji
from _io import TextIOWrapper

MIME = MimeTypes()

def try_file(name, content='[]') -> TextIOWrapper:
    """Check if a file exists and create it with default content if it doesnt"""
    try:
        return open(name)
    except FileNotFoundError:
        open(name, 'w').write(content)
        print(f'Generated {name} file')
        return open(name)

def quick_embed(ctx, title: str, description: str = None, colour: int = 0x023cfc) -> discord.Embed:
    """Creates an embed with a colour, title and description based on context"""
    try:
        colour = ctx.me.colour
    except AttributeError:
        pass
    return discord.Embed(title = title, description = description, colour = colour)

def embedable(url: str) -> bool:
    """checks if an item can be placed in a rich embed safeley"""
    url = pathname2url(url)
    mime_type = MIME.guess_type(url)
    return mime_type[0] in ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']

def emoji(estr: str) -> bool:
    """Checks if a string is an emoji"""
    #if the string is surrounded with <> there is a chance its a discord emoji
    if estr.startswith('<') and estr.endswith('>') and estr.count(':') == 2:
        estr = estr[3:] if estr.startswith('<a:') else estr[2:]
        while not estr.startswith(':'):
            estr = estr[1:]
        estr = estr[1:-1]
        if not estr:
            return True
        return False
    elif estr in uemoji:
        return True
    return False

def only_mentions_bot(bot, context) -> bool:
    """Checks if a string only contains a mention to the bot"""
    return context.content.strip() in [f'<@!{bot.user.id}>', f'<@{bot.user.id}>']
