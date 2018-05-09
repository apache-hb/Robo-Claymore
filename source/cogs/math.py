import discord
from discord.ext import commands
from .store import pyout

import mathutils
import math
from itertools import cycle

class Math:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Mathmatical calculations"
    description = "For executing supported math calculations"
    hidden = True

    @commands.command(name="inoutcircle")
    async def _inoutcircle(self, ctx, radius: int, x: int, y: int):
        await ctx.send(radius > math.sqrt(x^2 + y^2))

    @commands.command(name="sqrt")
    async def _sqrt(self, ctx, a: int):
        await ctx.send(math.sqrt(a))

    @commands.command(name="solve")
    async def _solve(self, ctx, equation: str):
        temp = []
        for a in equation:
            if a in ['+','-','/','*','%','^']:
                if a:
                    pass
            temp.append(a)

        if '^' in equation:
            temp = equation.split('^')
            a = float(temp[0])
            b = float(temp[1])
            #using ^ instead of ** breaks stuff
            await ctx.send(a**b)
            #TODO alot more math functions
            #and more complex stuff as well

    @commands.command(name="round")
    async def _round(self, ctx, a: int, b: float):
        await ctx.send('%.{}f'.format(a) % b)

def setup(bot):
    bot.add_cog(Math(bot))