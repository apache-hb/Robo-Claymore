from claymore.utils import wheel

from discord.ext.commands import command

from random import choice

class Fun(wheel(desc = 'fun commands')):
    @command()
    async def coinflip(self, ctx):
        pass

    @command()
    async def rate(self, ctx, *, thing: str):
        pass

    @command(
        brief = 'ask the magic 8ball a question',
        aliases = [ '8', '8ball' ]
    )
    async def magic(self, ctx):
        pass

    @command()
    async def rank(self, ctx, *, items: str):
        pass

def setup(bot):
    bot.add_cog(Fun(bot))