import discord
from discord.ext import commands
import sqlite3
from claymore import Wheel

class Owner(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

    async def cog_check(self, ctx):
        if ctx.author.id == self.bot.owner:
            return True
        await ctx.send('Come back with a warrant')
        return False

    @commands.command(name = 'shutdown')
    async def _shutdown(self, ctx):
        await self.bot.cleanup()

    @commands.command(name = 'test')
    async def _test(self, ctx):
        await ctx.send(embed = ctx.make_embed(title = 'A', description = 'B'))

    @commands.command(name = 'query')
    async def _query(self, ctx, *, query: str):
        try:
            await ctx.send(ctx.bot.execute(query).fetchone())
        except Exception as e:
            await ctx.send(e)

def setup(bot):
    bot.add_cog(Owner(bot))