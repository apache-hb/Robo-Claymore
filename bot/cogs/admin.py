from discord.ext.commands.core import guild_only, has_permissions
from claymore.utils import wheel
from discord.ext.commands import command

class Admin(wheel(desc = 'server administration tools')):
    @command(
        brief = 'remove messages from the current channel',
        aliases = [ 'prune', 'erase' ],
        help = """
        // remove 10 messages from the current channel
        &purge 10
        """
    )
    @has_permissions(manage_messages = True)
    @guild_only()
    async def purge(self, ctx, amount: int):
        if amount not in range(1, 100):
            return await ctx.send('must remove between 1 and 100 messages')

        await ctx.channel.delete_messages([msg async for msg in ctx.history(limit = amount, before = ctx.message)])
        await ctx.send(f'{ctx.author.mention} purged {amount} messages')

    @command()
    @guild_only()
    @has_permissions(administrator = True)
    async def prefix(self, ctx, it: str = None):
        if it:
            self.db.config.update(
                { 'id': ctx.guild.id },
                { 'id': ctx.guild.id, 'prefix': it },
                upsert = True
            )
            await ctx.send(f'set the custom prefix to `{it}`')
        else:
            self.db.config.update(
                { 'id': ctx.guild.id },
                { '$unset': { 'prefix': 1 } },
                upsert = True
            )
            await ctx.send(f'removed the custom prefix')

def setup(bot):
    bot.add_cog(Admin(bot))