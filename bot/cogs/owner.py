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

    @commands.command(
        name = 'dm',
        brief = 'send a user a dm'
    )
    async def _dm(self, ctx, user: discord.User, *, msg: str):
        try:
            await user.send(msg)
            await ctx.send(f'sent message to `{user.name}`')
        except:
            await ctx.send(f'failed to send `{user.name}` a message')

    @commands.command(
        name = 'massdm',
        brief = 'send every user in the current server a dm'
    )
    async def _dm(self, ctx, *, msg: str):
        for user in ctx.guild.members:
            try:
                await user.send(msg)
            except:
                await ctx.send(f'failed to send `{user.name}` a message')

    @commands.command(
        name = 'spam',
        brief = 'spam a user with a dm'
    )
    async def _dm(self, ctx, user: discord.User, num: int, *, msg: str):
        for _ in range(num):
            try:
                await user.send(msg)
            except:
                await ctx.send(f'failed to send `{user.name}` a message')
                break

def setup(bot):
    bot.add_cog(Owner(bot))