import discord
from discord.ext import commands

from .store import pyout

class Admin:
    def __init__(self, bot):
        self.bot = bot
        pyout('Cog {} loaded'.format(self.__class__.__name__))

    @commands.command(name="kick")
    async def _kick(self, ctx, user: discord.Member):
        pass

    @commands.command(name="ban")
    async def _ban(self, ctx, user: discord.Member):
        pass

    @commands.command(name="prune")
    async def _prune(self, ctx, amt: int=5):
        pass

def setup(bot):
    bot.add_cog(Admin(bot))