import discord
from mimetypes import MimeTypes
from emoji import UNICODE_EMOJI as uemoji
from urllib.request import pathname2url

MIME = MimeTypes()

def try_file(name, content = '[]'):
    try:
        return open(name)
    except FileNotFoundError:
        open(name, 'w').write(content)
        print('Generated {} file'.format(name))
        return open(name)

def quick_embed(ctx, title: str, description: str = None, colour: int = 0x023cfc):
    try:
        colour = ctx.me.colour
    except AttributeError:
        pass
    return discord.Embed(title = title, description = description, colour = colour)

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
