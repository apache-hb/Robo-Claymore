import discord
from discord.ext import commands

import random
from .utils.saved_dict import SavedDict
from .utils.shortcuts import quick_embed

class Anon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.names = SavedDict('cogs/store/anon_list.json', content = '{}')
        print(f'cog {self.__class__.__name__} loaded')

    @commands.group(name = "global")
    async def _global(self, ctx):
        pass

    @commands.command(name = "randacc")
    async def _randacc(self, ctx, platform: str):
        person = random.choice(self.names.data)

        embed = quick_embed(ctx, title = 'random user account')

        for account in person:
            embed.add_field(name = account['platform'], value = account['name'])

        await ctx.send(embed = embed)

    @commands.command(name = "addacc")
    async def _addacc(self, ctx, platform: str, *, name: str):
        if str(ctx.author.id) not in self.names.data:
            self.names[str(ctx.author.id)] = {}
        
        self.names[str(ctx.author.id)][platform.lower()] = name

        await ctx.send('added account')
        

    @_global.after_invoke
    @_randacc.after_invoke
    @_addacc.after_invoke
    async def _after(self, _):
        self.names.save()

def setup(bot):
    bot.add_cog(Anon(bot))