import discord
from discord.ext import commands

class Context(commands.context.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_embed(self, title, description, colour = 0x023cfc) -> discord.Embed:
        try:
            colour = self.me.colour
        except AttributeError:
            pass
        return discord.Embed(title = title, description = description, colour = colour)