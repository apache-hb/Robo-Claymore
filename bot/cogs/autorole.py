import discord
from discord.ext import commands
from random import choice
from claymore import Wheel

class Autorole(Wheel):
    def desc(self):
        return 'automatically give new users roles'

    def __init__(self, bot):
        super().__init__(bot)
        self.bot.add_listener(self.on_member_join)

    async def on_member_join(self, member):
        roles = await self.db.autorole.find_one({ 'id': member.guild.id })
        if roles:
            guild = self.bot.get_guild(roles['id'])
            if roles.get('random', False):
                roles = [choice(roles['roles'])]
            else:
                roles = roles['roles']

            await member.edit(roles = [guild.get_role(r) for r in roles])

    async def cog_check(self, ctx):
        if ctx.author.permissions_in(ctx.channel).administrator or ctx.author.id == self.bot.owner_id:
            return True
        await ctx.send('You need to be an admin to use this command')
        return False

    @commands.group(
        name = 'autorole',
        brief = 'manage all current server autoroles',
        invoke_without_command = True
    )
    async def _autorole(self, ctx):
        auto = await self.db.autorole.find_one({ 'id': ctx.guild.id })
        if auto is not None and auto['roles']:
            roles = auto['roles']
            embed = ctx.make_embed(title = 'Autoroles', description = f'There are currently {len(roles)} in the autoroles list')
            for role in roles:
                try:
                    r = ctx.guild.get_role(role)
                    embed.add_field(name = r.name, value = r.id)
                except:
                    roles.remove(role)

            await ctx.send(embed = embed)
            await self.db.autorole.update(
                { 'id': ctx.guild.id }, 
                { 'id': ctx.guild.id, 'roles': roles }, 
                upsert = True
            )
        else:
            await ctx.send(embed = ctx.make_embed(title = 'Autoroles', description = 'No current autoroles'))

    @_autorole.group(
        name = 'random',
        brief = 'configure autorole randomization for new members',
        invoke_without_command = True
    )
    async def _autorole_toggle(self, ctx, new: str):
        auto = await self.db.autorole.select_one({ 'id': ctx.guild.id })
        if auto is not None:
            await ctx.send(f'Randomized autorole is `{"enabled" if auto["random"] else "disabled"}`')
        else:
            await ctx.send('This server currently doesnt have any autoroles')

    @_autorole_toggle.command(
        name = 'enable',
        brief = 'enable autorole randomization for the current server'
    )
    async def _autorole_toggle_enable(self, ctx):
        await self.db.autorole.insert({ 'id': ctx.guild.id }, { 'id': ctx.guild.id, 'random': True }, upsert = True)
        await ctx.send('Enaabled autorole randomization')

    @_autorole_toggle.command(
        name = 'disable',
        brief = 'disable autorole randomization for the current server'
    )
    async def _autorole_toggle_disable(self, ctx):
        await self.db.autorole.update({ 'id': ctx.guild.id }, { 'id': ctx.guild.id, 'random': False }, upsert = True)
        await ctx.send('Disabled autorole randomization')

    @_autorole.command(
        name = 'add',
        brief = 'add an role to the autorole list'
    )
    async def _autorole_add(self, ctx, role: discord.Role):
        await self.db.autorole.update(
            { 'id': ctx.guild.id },
            { '$push': { 'roles': role.id }, '$set': { 'random': False } },
            upsert = True
        )
        await ctx.send(f'Added {role.name} as an autorole')

    @_autorole.command(
        name = 'remove',
        brief = 'remove a role from the autorole list'
    )
    async def _autorole_remove(self, ctx, role: discord.Role):
        await self.db.autorole.update(
            { 'id': ctx.guild.id },
            { '$pull': { 'roles': { '$in': [ role.id ] } } }
        )
        await ctx.send(f'Removed {role.name} from autorole list')

    @_autorole.command(
        name = 'reset',
        brief = 'remove all autoroles from the current server',
        aliases = [ 'wipe', 'purge', 'clean' ]
    )
    async def _autorole_reset(self, ctx):
        await self.db.autorole.remove({ 'id': ctx.guild.id })
        await ctx.send('Removed all autoroles')

async def setup(bot):
    await bot.add_cog(Autorole(bot))