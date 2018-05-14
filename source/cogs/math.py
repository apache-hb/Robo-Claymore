import discord
from discord.ext import commands

import mathutils
import math

class Math:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Mathmatical calculations"
    description = "For executing supported math calculations"
    hidden = True

    #look, i know it's really specific
    #but i got some math homework with a formula thats half a mile
    #so this is going in here
    @commands.command(name="pointtoline")
    async def _pointtoline(self, ctx, x: float, y: float, m: float, k: float):
        await ctx.send(math.sqrt((((x+m*y-m*k)/(m**2) +1)-x)**2 + ((m * (x + (m * y) - m * k)/(m**2)) +k -y)**2))

    @commands.command(name="equationfrompoints")
    async def _equationfrompoints(self, ctx, x1, y1, x2, y2):
        m = ((y2-y1)/(x2-x1))

    @commands.command(name="inoutcircle")
    async def _inoutcircle(self, ctx, radius: int, locx: int, locy: int):
        await ctx.send(radius > math.sqrt(locx ^ 2 + locy ^ 2))

    @commands.command(name="sqrt")
    async def _sqrt(self, ctx, todo: int):
        await ctx.send(math.sqrt(todo))

    @commands.command(name="simplesolve")
    async def _simplesolve(self, ctx, equation: str):
        if not set(['^', '**']).isdisjoint(equation):
            equation = equation.split('^')
            ret = float(equation[0])
            for a in equation[1:]:
                ret **= float(a)
            return await ctx.send(ret)

        elif '+' in equation:
            equation = equation.split('+')
            ret = float(equation[0])
            for a in equation[1:]:
                ret += float(a)
            return await ctx.send(ret)

        elif '-' in equation:
            equation = equation.split('-')
            ret = float(equation[0])
            for a in equation[1:]:
                ret -= float(a)
            return await ctx.send(ret)

        elif '*' in equation:
            equation = equation.split('*')
            ret = float(equation[0])
            for a in equation[1:]:
                ret *= float(a)
            return await ctx.send(ret)

        elif '/' in equation:
            equation = equation.split('/')
            ret = float(equation[0])
            for a in equation[1:]:
                ret /= float(a)
            return await ctx.send(ret)

        else:
            return await ctx.send(
                'must be simple\none operation type per calculation')

    @commands.command(name="solve")
    async def _solve(self, ctx, equation: str):
        temp = []

        for elem in equation:
            thiselem = elem

            if thiselem in ['+', '-', '/', '*', '^', '%', '(', ')']:
                elem0 = elem
                # TODO there has to be abetter way of doing this
                # also, miss me with that itertools shit
                try:
                    elem1 = equation[equation.index(elem) + 1]
                except IndexError:
                    elem1 = None

                try:
                    elem2 = equation[equation.index(elem) + 2]
                except IndexError:
                    elem2 = None

                try:
                    elem3 = equation[equation.index(elem) + 3]
                except IndexError:
                    elem3 = None

                try:
                    elem4 = equation[equation.index(elem) + 4]
                except IndexError:
                    elem4 = None

                try:
                    elem5 = equation[equation.index(elem) + 5]
                except IndexError:
                    elem5 = None
                if elem0 == '*' and elem1 == '*':
                    temp.append('**')
                elif elem0 + elem1 + elem2 + elem3 == 'sqrt':
                    if not '(' in [elem4, elem5]:
                        return await ctx.send(
                            'sqrt must be used with braces\nfor example ```\nsqrt(5)```works properly'
                        )
                    else:
                        temp.append('sqrt')
                        temp.append('(')
        '''
        if '^' in equation:
            temp = equation.split('^')
            a = float(temp[0])
            b = float(temp[1])
            #using ^ instead of ** breaks stuff
            await ctx.send(a**b)
            #TODO alot more math functions
            #and more complex stuff as well'''

    @commands.command(name="round")
    async def _round(self, ctx, a: int, b: float):
        await ctx.send('%.{}f'.format(a) % b)


def setup(bot):
    bot.add_cog(Math(bot))
