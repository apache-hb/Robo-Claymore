import discord
from discord.ext import commands
from random import choice
from claymore import Wheel
import pymongo

class Autorole(Wheel):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot.add_listener(self.on_member_join)

    async def on_member_join(self, member):
        roles = self.db.autorole.find_one({ 'id': member.guild.id })
        if roles:
            guild = self.bot.get_guild(roles['id'])
            if roles['random']:
                roles = [choice(roles['roles'])]
            else:
                roles = roles['roles']

            await member.edit(roles = [guild.get_role(r) for r in roles])

    async def cog_check(self, ctx):
        if ctx.author.permissions_in(ctx.channel).administrator or ctx.author.id == self.bot.owner:
            return True
        await ctx.send('You need to be an admin to use this command')
        return False

    @commands.group(
        name = 'autorole',
        invoke_without_command = True
    )
    async def _autorole(self, ctx):
        auto = self.db.autorole.find_one({ 'id': ctx.guild.id })
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
            self.db.autorole.update({ 'id': ctx.guild.id }, { 'id': ctx.guild.id, 'roles': roles }, upsert = True)
        else:
            await ctx.send(embed = ctx.make_embed(title = 'Autoroles', description = 'No current autoroles'))

    @_autorole.group(
        name = 'random',
        invoke_without_command = True
    )
    async def _autorole_toggle(self, ctx, new: str):
        auto = self.db.autorole.select_one({ 'id': ctx.guild.id })
        if auto is not None:
            await ctx.send(f'Randomized autorole is `{"enabled" if auto["random"] else "disabled"}`')
        else:
            await ctx.send('This server currently doesnt have any autoroles')

    @_autorole_toggle.command(name = 'enable')
    async def _autorole_toggle_enable(self, ctx):
        self.db.autorole.insert({ 'id':ctx.guild.id }, { 'id': ctx.guild.id, 'random': True }, upsert = True)
        await ctx.send('Enaabled autorole randomization')

    @_autorole_toggle.command(name = 'disable')
    async def _autorole_toggle_disable(self, ctx):
        self.db.autorole.update({ 'id':ctx.guild.id }, { 'id': ctx.guild.id, 'random': False }, upsert = True)
        await ctx.send('Disabled autorole randomization')

    @_autorole.command(name = 'add')
    async def _autorole_add(self, ctx, role: discord.Role):
        self.db.autorole.update(
            { 'id': ctx.guild.id },
            { '$push': { 'roles': role.id }, '$set': { 'random': False } },
            upsert = True
        )
        await ctx.send(f'Added {role.name} as an autorole')

    @_autorole.command(name = 'remove')
    async def _autorole_remove(self, ctx, role: discord.Role):
        self.db.autorole.update(
            { 'id': ctx.guild.id },
            { '$pull': { 'roles': { '$in': [ role.id ] } } }
        )
        await ctx.send(f'Removed {role.name} from autorole list')

    @_autorole.command(
        name = 'reset',
        aliases = [ 'wipe', 'purge', 'clean' ]
    )
    async def _autorole_reset(self, ctx):
        self.db.autorole.remove(
            { 'id': ctx.guild.id }
        )
        await ctx.send('removed all autoroles')

def setup(bot):
    bot.add_cog(Autorole(bot))