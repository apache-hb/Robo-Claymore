import discord
from discord.ext import commands

import aiohttp
from .store import Store, style_embed, shorten_url

class Utility:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Miscellaneous functions"
    description = "FOr extras that don\'t fit in"
    hidden = True

    @commands.command(name="wolfram")
    async def _wolfram(self, ctx, *, query: str=None):
        pass

    @commands.command(name="shorten")
    async def _shorten(self, ctx, *, url: str=None):
        if not url is None:
            return await ctx.send(await shorten_url(long_url=url))
        return await ctx.send('You need to enter a url')

    @commands.command(name="embed")
    async def _embed(self, ctx, *, content: str=None):
        pass

def setup(bot):
    bot.add_cog(Utility(bot))