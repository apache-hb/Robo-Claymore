import discord
from discord.ext import commands
from claymore import Wheel

class Admin(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

    async def cog_check(self, ctx):
        if ctx.author.permissions_in(ctx.channel).administrator or ctx.author.id == self.bot.owner:
            return True
        await ctx.send('You need to be an admin to use this command')
        return False

    @commands.group(
        name = 'prefix',
        invoke_without_command = True
    )
    async def _prefix(self, ctx):
        prefix = await self.bot.get_prefix(ctx.message)
        await ctx.send(f'Current prefix is `{prefix[0]}`')

    @_prefix.command('update')
    async def _prefix_update(self, ctx, prefix: str):
        self.db.prefix.insert_one({ 'id': ctx.guild.id , 'prefix': prefix })
        await ctx.send(f'New prefix is now `{prefix}`')

    @_prefix.command('reset')
    async def _prefix_reset(self, ctx):
        self.db.prefix.delete_one({ 'id': ctx.guild.id })
        await ctx.send(f'Reset prefix to `{self.bot.config["discord"]["prefix"]}`')

def setup(bot):
    bot.add_cog(Admin(bot))