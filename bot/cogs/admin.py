import discord
from discord.ext import commands
from claymore import Wheel

class Admin(Wheel):
    def desc(self):
        return 'admin and moderation commands'

    async def cog_check(self, ctx):
        if ctx.author.permissions_in(ctx.channel).administrator or ctx.author.id == self.bot.owner_id:
            return True
        await ctx.send('You need to be an admin to use this command')
        return False

    @commands.group(
        name = 'prefix',
        brief = 'manage bots prefix on the current server',
        invoke_without_command = True
    )
    async def _prefix(self, ctx):
        prefix = await self.bot.get_prefix(ctx.message)
        if isinstance(prefix, tuple):
            prefix = '(' + ' | '.join(prefix) + ')'
        await ctx.send(f'Current prefix is `{prefix}`')

    @_prefix.command(
        name = 'update',
        brief = 'update server prefix to a new prefix'
    )
    async def _prefix_update(self, ctx, prefix: str):
        await self.db.prefix.update(
            { 'id': ctx.guild.id }, 
            { 'id': ctx.guild.id, 'prefix': prefix }, 
            upsert = True
        )
        await ctx.send(f'New prefix is now `{prefix}`')

    @_prefix.command(
        name = 'reset',
        brief = 'reset server prefix to the default prefix'
    )
    async def _prefix_reset(self, ctx):
        await self.db.prefix.delete_one({ 'id': ctx.guild.id })
        await ctx.send(f'Reset prefix to `{self.bot.config["discord"]["prefix"]}`')

    @commands.command(
        name = 'hackban',
        brief = 'ban someone not on the server by userid'
    )
    async def _hackban(self, ctx, user: int):
        try:
            await ctx.guild.ban(discord.Object(id = user))
        except Exception:
            return await ctx.send(f'Failed to ban `{user}`')

        await ctx.send(f'Banned user with id of `{user}`')

async def setup(bot):
    await bot.add_cog(Admin(bot))
