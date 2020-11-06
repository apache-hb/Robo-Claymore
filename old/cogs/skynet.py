import json
import os
import time
from discord.ext import commands

from .utils.shortcuts import try_file

class SkyNet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        print(f'cog {self.__class__.__name__} loaded')

    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        #ignore obvious bot commands
        if ctx.content.startswith(('!', '&', '/', '*', '$', '#')):
            return

        if ctx.guild is None:
            new = 'cogs/store/skynet/messages/'
        else:
            new = f'cogs/store/skynet/{ctx.guild.id}/'

        os.makedirs(new, exist_ok = True)

        ret = json.load(try_file(new + f'{ctx.channel.id}.json'))
        ret.append({
            'content': ctx.content,
            'meta': {
                'user': ctx.author.id,
                'name': ctx.author.name,
                'time': time.time()
            }
        })
        json.dump(ret, open(new + f'{ctx.channel.id}.json', 'w'), indent = 4)


def setup(bot):
    bot.add_cog(SkyNet(bot))
