import discord
from discord.ext import commands
from claymore import Wheel

class Owner(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

    async def cog_check(self, ctx):
        if ctx.author.id == self.bot.owner:
            return True
        await ctx.send('Come back with a warrant')
        return False

    @commands.command(name = 'shutdown')
    async def _shutdown(self, ctx):
        await self.bot.close()

    @commands.command(name = 'test')
    async def _test(self, ctx, num: int):
        self.db.test.insert_one({ 'name': 'test', 'val': num })

    @commands.command(name = 'query')
    async def _query(self, ctx, *, query: str):
        pass

def setup(bot):
    bot.add_cog(Owner(bot))