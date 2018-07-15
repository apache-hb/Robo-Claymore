import discord
from discord.ext import commands
import json
from .store import can_override, quick_embed


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.autorole_list = json.load(open('cogs/store/autorole.json'))
        self.hidden = False
        print('Cog {} loaded'.format(self.__class__.__name__))

    def is_admin():
        async def predicate(ctx):
            if not ctx.author.permissions_in(ctx.channel).administrator or not await can_override(ctx):
                await ctx.send('You dont have the required admin permissions')
                return False
            return True
        return commands.check(predicate)

    def can_kick():
        async def predicate(ctx):
            if not ctx.author.permissions_in(ctx.channel).kick_members or not await can_override(ctx):
                await ctx.send('You dont have the permission to kick')
                return False
            return True
        return commands.check(predicate)

    def can_ban():
        async def predicate(ctx):
            if not ctx.author.permissions_in(ctx.channel).ban_members or not await can_override(ctx):
                await ctx.send('You dont have the permission to ban')
                return False
            return True
        return commands.check(predicate)

    def manage_messages():
        async def predicate(ctx):
            if not ctx.author.permissions_in(ctx.channel).manage_messages or not await can_override(ctx):
                await ctx.send('You dont have the permission to delete messages')
                return False
            return True
        return commands.check(predicate)

    def manage_nicknames():
        async def predicate(ctx):
            if not ctx.author.permissions_in(ctx.channel).manage_nicknames or not await can_override(ctx):
                await ctx.send('You dont have the permission to manage nicknames')
                return False
            return True
        return commands.check(predicate)

    async def will_manage(self, ctx, user: discord.Member, kind: str):
        if not await can_override(ctx, user):
            await ctx.send('I dont want to {} them'.format(kind))
            return False
        elif user.id == self.bot.user.id:
            await ctx.send('I dont want to {} myself'.format(kind))
            return False
        elif user.id == ctx.author.id:
            await ctx.send('I wont let you {} yourself'.format(kind))
            return False
        if user.permissions_in(ctx.channel).administrator:
            await ctx.send('I wont {} admins'.format(kind))
            return False
        else:
            return True

    @commands.command(name = "kick")
    @commands.guild_only()
    @can_kick()
    async def _kick(self, ctx, user: discord.Member):
        if not await self.will_manage(ctx, user, 'kick'):
            return

        try:
            await user.kick()
        except discord.errors.Forbidden:
            await ctx.send('I dont have the correct permissions to kick him')
        else:
            await ctx.send('So long sucker')

    @commands.command(name = "ban", aliases = ['yeet'])
    @commands.guild_only()
    @can_ban()
    async def _ban(self, ctx, user: discord.Member):
        if not await self.will_manage(ctx, user, 'ban'):
            return

        try:
            await user.ban(delete_message_days = 7, reason = 'Softban by {}'.format(ctx.author))
        except discord.errors.Forbidden:
            await ctx.send('I dont have the correct permissions to ban that user')
        else:
            await ctx.send('And their gone')

    @commands.command(name = "softban")
    @commands.guild_only()
    @can_kick()
    async def _softban(self, ctx, user: discord.Member):
        if not await self.will_manage(ctx, user, 'softban'):
            return

        try:
            await user.ban(delete_message_days = 7, reason = 'Softban by {}'.format(ctx.author))
            await asyncio.sleep(15)
            await user.unban(reason = 'Softban by {}'.format(ctx.author))
            await user.send(await ctx.channel.create_invite(max_uses = 1))
        except discord.errors.Forbidden:
            await ctx.send('I dont have the permissions to do that')
        else:
            await ctx.send('their gone now, But i have reinvited them')

    @commands.command(name = "clean")
    @commands.guild_only()
    @manage_messages()
    async def _clean(self, ctx, amount: int = 5):
        if not 5 <= amount <= 100:
            return await ctx.send('Amount must be between 5 and 100')

        try:
            await ctx.channel.purge(limit = amount)
        except discord.errors.Forbidden:
            await ctx.send('I dont have the permissions to delete messages')
        else:
            await ctx.send('{} messages have been purged'.format(amount))

    @commands.command(name = "massnick")
    @commands.guild_only()
    @manage_nicknames()
    async def _massnick(self, ctx, *, nickname: str = None):
        if not nickname is None:
            if not 2 <= len(nickname) <= 32:
                return await ctx.send('Nickname length must be between 2 and 32 characters')
            await ctx.send('Setting all nicknames to {}'.format(nickname))
        else:
            await ctx.send('Resetting nicknames')

        a = 0

        for member in ctx.guild.members:
            try:
                await member.edit(nick = nickname)
                a+=1
            except Exception:
                pass

        await ctx.send('massnicked {} users'.format(a))

    @commands.group(invoke_without_command = True)
    @commands.guild_only()
    @is_admin()
    async def autorole(self, ctx):
        for server in self.autorole_list:
            if server['server_id'] == ctx.guild.id:
                ret = ''
                if not server['roles']:
                    ret = 'This server has no autoroles'
                else:
                    for role in server['roles']:
                        ret += str(await discord.utils.get(ctx.guild.roles, id = role)) + '\n'

                embed = quick_embed(ctx, title = 'Autoroles')
                embed.add_field(name = 'All roles', value = ret)
                return await ctx.send(embed = embed)
        self.autorole_list.append({
            'server_id': user.guild.id,
            'roles': []
        })
        json.dump(self.autorole_list, open('cogs/store/autorole.json', 'w'), indent = 4)
        return await self.autorole(ctx)


    async def on_guild_role_delete(self, role):
        for server in self.autorole_list:
            if server['server_id'] == role.guild.id:
                if role.id in server['roles']:
                    server['roles'].remove(role.id)
                    json.dump(self.autorole_list, open('cogs/store/autorole.json', 'w'), indent = 4)

    async def on_member_join(self, user):
        for server in self.autorole_list:
            if server['server_id'] == user.guild.id:
                user_roles = user.roles
                bad_roles = []
                for role in server['roles']:
                    new_role = discord.utils.get(guild.roles, id = role)
                    user_roles.append(new_role)
                return await user.edit(roles = user_roles)
        self.autorole_list.append({
            'server_id': user.guild.id,
            'roles': []
        })
        json.dump(self.autorole_list, open('cogs/store/autorole.json', 'w'), indent = 4)
        return await self.on_member_join(user)

    #if kind is true it will add the autorole, otherwise it will try and delete it
    async def edit_autorole_list(self, ctx, role: discord.Role, kind: bool):
        for server in self.autorole_list:
            if server['server_id'] == ctx.guild.id:
                if kind:#adding an autorole
                    if role.id in server['roles']:
                        return await ctx.send('That role is already in the autorole list')

                    server['roles'].append(role.id)
                    json.dump(self.autorole_list, open('cogs/store/autorole.json', 'w'), indent = 4)
                    return await ctx.send('Added {} to the autorole list'.format(role))
                else:#removing an autorole
                    if not role.id in server['roles']:
                        return await ctx.send('That role is not an autorole')

                    server['roles'].remove(role.id)
                    json.dump(self.autorole_list, open('cogs/store/autorole.json', 'w'), indent = 4)
                    return await ctx.send('Removed {} from the autorole list'.format(role))
        self.autorole_list.append({
            'server_id': guild.id,
            'roles': []
        })
        json.dump(self.autorole_list, open('cogs/store/autorole.json', 'w'), indent = 4)
        return self.edit_autorole_list(guild, role, kind)


    @autorole.command(name = "add")
    @commands.guild_only()
    @is_admin()
    async def _autorole_add(self, ctx, role: discord.Role):
        return await self.edit_autorole_list(ctx, role, True)

    @autorole.command(name = "remove")
    @commands.guild_only()
    @is_admin()
    async def _autorole_remove(self, ctx, role: discord.Role):
       return await self.edit_autorole_list(ctx, role, False)

def setup(bot):
    bot.add_cog(Admin(bot))