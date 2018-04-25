import discord
from discord.ext import commands

import json
import aiohttp
from bs4 import BeautifulSoup

class Warframe:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Warframe info"
    description = "Get info about an item or event in warframe"
    hidden = True

    @commands.group(invoke_without_command=True)
    async def warframe(self, ctx):
        await ctx.send('soon™')

    @warframe.command(name="info")
    async def _info(self, ctx, *, item: str):
        pass #with urllib.request.urlopen('')

    @warframe.command(name="cetustime")
    async def _cetustime(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.warframestat.us/pc/cetusCycle') as resp:
                    await ctx.send(await resp.text())
                    print(await resp.text())
        except AttributeError:
            pass

def setup(bot):
    bot.add_cog(Warframe(bot))