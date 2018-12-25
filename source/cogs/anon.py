import discord
from discord.ext import commands

from .utils.saved_dict import SavedDict

class Anon:
    def __init__(self, bot):
        self.bot = bot
        self.names = SavedDict('cogs/store/anon_list.json', content = '{}')
        print(f'cog {self.__class__.__name__} loaded')

    @commands.group(name = "global")
    async def _global(self, ctx):
        pass

    @commands.command(name = "randacc")
    async def _randacc(self, ctx, platform: str):
        pass

    @commands.command(name = "addacc")
    async def _addacc(self, ctx, platform: str, *, name: str):
        pass

def setup(bot):
    bot.add_cog(Anon(bot))