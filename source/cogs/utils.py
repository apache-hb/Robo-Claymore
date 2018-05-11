import discord
import emoji
from time import time
import aiohttp
from mimetypes import MimeTypes
from emoji import UNICODE_EMOJI
from .store import whitelist
MIME = MimeTypes()


def can_override(bot, user):
    return bot.is_owner(user) or user in whitelist


def quick_embed(ctx, title: str, description: str = '',
                colour: int = 0xff1500):
    try:
        colour = ctx.guild.me.colour
    except AttributeError:
        pass
    embed = discord.Embed(title=title, description=description, colour=colour)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    return embed


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
    elif emoji in UNICODE_EMOJI:
        return True
    return False


def guild_template(guild):
    return {"server_id": guild.id, "first_joined": int(time()), "contents": []}


async def shorten_url(long_url: str):
    url = "http://tinyurl.com/api-create.php?url=" + long_url
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            return await response.text()


def is_embedable(url: str):
    url = pathname2url(url)
    mime_type = MIME.guess_type(url)
    return mime_type[0] in [
        'image/jpeg', 'image/png', 'image/gif', 'image/jpg'
    ]
