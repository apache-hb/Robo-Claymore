from discord import Role
from discord.ext.commands import guild_only, has_permissions, command, group
from claymore.utils import wheel

class Admin(wheel(desc = 'server administration tools')):
    def __init__(self, bot):
        super().__init__(bot)

        @bot.listen()
        async def on_member_join(member):
            if roles := await self.db.roles.find_one({ 'id': member.guild.id }):
                await member.edit(roles = [it for each in roles['roles'] if (it := member.guild.get_role(each))])

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
            await self.db.config.update_one(
                { 'id': ctx.guild.id },
                { '$set': { 'id': ctx.guild.id, 'prefix': it } },
                upsert = True
            )
            await ctx.send(f'set the custom prefix to `{it}`')
        else:
            await self.db.config.update_one(
                { 'id': ctx.guild.id },
                { '$unset': { 'prefix': 1 } },
                upsert = True
            )
            await ctx.send(f'removed the custom prefix')

    @group(
        aliases = [ 'autoroles' ],
        invoke_without_subcommand = False
    )
    @guild_only()
    async def autorole(self, ctx):
        if roles := await self.db.roles.find_one({ 'id': ctx.guild.id }):
            if it := [role for id in roles['roles'] if (role := ctx.guild.get_role(id))]:
                return await ctx.send(embed = ctx.embed('autoroles', f'{len(it)} total autoroles', {
                    'roles': ', '.join([role.mention for role in it])
                }))
        
        await ctx.send('this server has no autoroles')
        

    @autorole.command(
        name = 'add',
        aliases = [ 'push' ]
    )
    @has_permissions(administrator = True)
    async def autorole_add(self, ctx, role: Role):
        await self.db.roles.update_one(
            { 'id': ctx.guild.id },
            { '$set': { 'id': ctx.guild.id }, '$addToSet': { 'roles': role.id } },
            upsert = True
        )
        await ctx.send(f'added `{role.name}` to the autorole set')

    @autorole.command(
        name = 'remove',
        aliases = [ 'pull' ]
    )
    @has_permissions(administrator = True)
    async def autorole_remove(self, ctx, role: Role):
        await self.db.roles.update_one(
            { 'id': ctx.guild.id },
            { '$set': { 'id': ctx.guild.id }, '$pull': { 'roles': role.id } },
            upsert = True
        )
        await ctx.send(f'removed `{role.name}` from the autorole set')

    @autorole.command(
        name = 'reset',
        aliases = [ 'wipe', 'clear' ]
    )
    @has_permissions(administrator = True)
    async def autorole_reset(self, ctx):
        await self.db.roles.update_one(
            { 'id': ctx.guild.id },
            { '$set': { 'id': ctx.guild.id, 'roles': [] } },
            upsert = True
        )
        await ctx.send('removed all autoroles')

def setup(bot):
    bot.add_cog(Admin(bot))