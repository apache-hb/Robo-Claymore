from claymore import Wheel
import discord
from discord.ext import commands
import random
from random import choice, randint

BALL_OPTIONS = [
    'Yes',
    'Outlook good',
    'Almost certainly',
    'Without a doubt',
    'Definetly',

    'No',
    'Not likely',
    'Probably not',
    'Definetly not',
    'Not a chance'
]

class Fun(Wheel):
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

    @commands.command(name = '8ball')
    async def _8ball(self, ctx, *, thing: str):
        await ctx.send(choice(BALL_OPTIONS))

    @commands.command(name = 'rate')
    async def _rate(self, ctx, *, thing: str):
        await ctx.send(f'I\'d rate {thing} at {randint(0, 10)}/10')

def setup(bot):
    bot.add_cog(Fun(bot))