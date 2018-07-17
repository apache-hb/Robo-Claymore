import discord
import aiohttp
from urllib.request import pathname2url
from mimetypes import MimeTypes
from emoji import UNICODE_EMOJI as uemoji

MIME = MimeTypes()

def try_file(name, content = '[]'):
    try:
        return open(name)
    except FileNotFoundError:
        open(name, 'w').write(content)
        print('Generated {} file'.format(name))
        return open(name)

async def can_override(ctx, user = None):
    if user is None:
        user = ctx.author
    return await ctx.bot.is_owner(user) or user.id in whitelist

def quick_embed(ctx, title: str, description: str = None, colour: int = 0x023cfc):
    try:
        colour = ctx.me.colour
    except AttributeError:
        pass
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

async def url_request(**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(**kwargs) as resp:
            return await resp.text()

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

def only_mentions_bot(bot, context):

    if context.content.strip() == '<@!{}>'.format(bot.user.id):
        return True

    elif context.content.strip() == '<@{}>'.format(bot.user.id):
        return True

    return False

blacklist = json.load(try_file('cogs/store/blacklist.json'))