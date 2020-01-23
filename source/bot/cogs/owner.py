import discord
from discord.ext import commands
from claymore import Wheel, PagedEmbed

class Owner(Wheel):
    def desc(self):
        return 'owner only commands'
        
    def hidden(self):
        return True
    
    async def cog_check(self, ctx):
        if await self.bot.is_owner(ctx.author):
            return True
        await ctx.send('Come back with a warrant')
        return False

    @commands.command(
        name = 'shutdown',
        brief = 'shutdown the bot'
    )
    async def _shutdown(self, ctx):
        await self.bot.close()

    @commands.command(
        name = 'setname',
        brief = 'set the bots current name'
    )
    async def _setname(self, ctx, *, name: str):
        await self.bot.edit(username = name)

    @commands.command(
        name = 'setactivity',
        brief = 'set the bots current activity'
    )
    async def _setactivity(self, ctx, *, text: str):
        await self.bot.change_presence(activity = discord.Game(text))

def setup(bot):
    bot.add_cog(Owner(bot))