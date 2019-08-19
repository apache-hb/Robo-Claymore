import discord
from discord.ext import commands
from claymore import Wheel, PagedEmbed

class Owner(Wheel):
    async def cog_check(self, ctx):
        if await self.bot.is_owner(ctx.author):
            return True
        await ctx.send('Come back with a warrant')
        return False

    @commands.command(name = 'shutdown')
    async def _shutdown(self, ctx):
        await self.bot.close()

    @commands.command(name = 'setname')
    async def _setname(self, ctx, *, name: str):
        await self.bot.edit(username = name)

    @commands.command(name = 'setactivity')
    async def _setactivity(self, ctx, *, text: str):
        await self.bot.change_presence(activity = discord.Game(text))

def setup(bot):
    bot.add_cog(Owner(bot))