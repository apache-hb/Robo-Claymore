import discord
from discord.ext.commands import command, Cog

class Help(Cog):
    brief = 'Get detailed help for each command'
    description = ''' 
    Provides all the help and documentation you could ever need.
    Every module, group and command comes with a description of 
    its use and function as well as detailed explanations of
    how to properly use each command.'''
    version = '0.0.1'

    def __init__(self, bot):
        self.bot = bot
        print(f'cog {self.__class__.__name__} loaded')

    @command(name = 'help')
    async def _help(self, ctx, name: str = None):
        if name is None:
            await ctx.send(name)
        else:
            await ctx.send(name)

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))