from claymore import Wheel
import discord
from discord.ext import commands
import random

class Fun(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name = 'clap')
    async def _clap(self, ctx, *, text: str):
        await ctx.send(' :clap: '.join(text.split(' ')))

    @commands.command(name = 'randomcase')
    async def _randomcase(self, ctx, *, text: str):
        await ctx.send(''.join(random.choice((str.upper, str.lower))(x) for x in text))

    @commands.command(name = 'sawpcase')
    async def _swapcase(self, ctx, *, text: str):
        await ctx.send(text.swapcase())

    @commands.command(name = 'reverse')
    async def _reverse(self, ctx, *, text: str):
        await ctx.send(text[::-1])

def setup(bot):
    bot.add_cog(Fun(bot))