import discord
import emoji
from time import time


def quick_embed(ctx, title: str, description: str='', colour: int=0xff1500):
    try: colour = ctx.guild.me.colour
    except AttributeError: pass
    embed = discord.Embed(title=title, description=description, colour=colour)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    return embed

def is_emoji(target: str):
    pass

def guild_template(guild):
    return {
        "server_id": guild.id,
        "first_joined": int(time()),
        "contents": []
    }