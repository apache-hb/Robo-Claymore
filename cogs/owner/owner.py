
from discord.ext.commands import command
import subprocess

class Owner:
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
        proc = subprocess.Popen(['git', 'pull'], stdout = subprocess.PIPE)
        
        output = proc.communicate()[0]

    async def on_ready(self):
        print(f'Bot loaded: {self.bot.user.name}#{self.bot.user.discriminator}')