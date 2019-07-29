import discord
from discord.ext import commands
from claymore import Wheel

class Admin(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

        #custom prefixes per server
        self.bot.execute(
            """
            CREATE TABLE IF NOT EXISTS custom_prefixes (
                id INT NOT NULL,
                prefix TEXT NOT NULL,
                PRIMARY KEY(id)
            );
            """
        )

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
    async def _prefix_update(self, ctx, prefix):
        self.insert().or_replace_into('custom_prefixes').values(id = ctx.guild.id, prefix = prefix).execute()
        await ctx.send(f'Prefix has been set to `{prefix}`')

    @_prefix.command('reset')
    async def _prefix_reset(self, ctx):
        self.delete()._from('custom_prefixes').where('id').equals(ctx.guild.id).execute()
        prefix = await self.bot.get_prefix(ctx.message)
        await ctx.send(f'Prefix has been reset to `{prefix[0]}`')

def setup(bot):
    bot.add_cog(Admin(bot))