
from ..internal import Cog, Ranks

from discord.ext.commands import command
import subprocess
import os
import sys

class Owner(Cog):
    def visibility() -> int:
        return Ranks.privillige | Ranks.owner

    def __init__(self, bot):
        self.bot = bot
        print(f'cog {self.__class__.__name__} loaded')

    async def __local_check(self, ctx):
        if await self.bot.is_owner(ctx.author):
            return True
        await ctx.send('Go away')
        return False

    @command(
        name = 'test',
        description = 'A quick commands to make sure the bot is functional',
        brief = 'Is this thing on?'
    )
    async def _test(self, ctx):
        await ctx.send('Working!')

    @command(
        name = 'restart',
        description = 'Restart the bot and apply updates from github',
        brief = 'Have you tried turning it off and on again?'
    )
    async def _restart(self, ctx):

        #pull from source
        proc = subprocess.Popen(['git', 'pull'], stdout = subprocess.PIPE)
        
        output = proc.communicate()[0]
        await ctx.send('```diff\n' + output.decode('utf-8') + '```')

        await ctx.send('Restarting...')

        #restart the python executable
        python = sys.executable
        os.execl(python, python, *sys.argv)

