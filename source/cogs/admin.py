import json

import discord
from discord.ext import commands

from .utils import checks
from .utils.checks import can_override
from .utils.shortcuts import quick_embed, try_file
from .utils.saved_dict import SavedDict

class Admin:
    def __init__(self, bot):
        self.bot = bot
        #FIXME replace all dicts with savedDict
        self.server_blacklists = SavedDict('cogs/store/server_blacklist.json', content = '{}')
        self.autorole_list = json.load(try_file('cogs/store/autorole.json', content = '{}'))
        self.leave_channels = json.load(try_file('cogs/store/leave.json', content = '{}'))
        self.command_blacklist = json.load(try_file('cogs/store/command_blacklist.json', content = '{}'))
        print(f'cog {self.__class__.__name__} loaded')

    async def will_manage(self, ctx, user: discord.Member, kind: str):
        if await can_override(ctx, user):
            await ctx.send(f'I dont want to {kind} them')
            return False
        elif user.id == self.bot.user.id:
            await ctx.send(f'I dont want to {kind} myself')
            return False
        elif user.id == ctx.author.id:
            await ctx.send(f'I wont let you {kind} yourself')
            return False
        if user.permissions_in(ctx.channel).administrator:
            await ctx.send(f'I cant {kind} admins')
            return False
        else:
            return True

    @commands.command(
        name = "kick",
        description = "kick a user from the current server",
        brief = "they'll be back"
    )
    @commands.guild_only()
    @checks.can_kick()
    async def _kick(self, ctx, user: discord.Member):
        if not await self.will_manage(ctx, user, 'kick'):
            return

        try:
            await user.kick()
        except discord.errors.Forbidden:
            await ctx.send('I dont have the correct permissions to kick him')
        else:
            await ctx.send('So long sucker')

    @commands.command(
        name = "ban",
        aliases = ['yeet'],
        description = "permentantly ban a user from the current server",
        brief = "so long sucker"
    )
    @commands.guild_only()
    @checks.can_ban()
    async def _ban(self, ctx, user: discord.Member):
        if not await self.will_manage(ctx, user, 'ban'):
            return

        try:
            await user.ban(delete_message_days = 7, reason = f'ban by {ctx.author}')
        except discord.errors.Forbidden:
            await ctx.send('I dont have the correct permissions to ban that user')
        else:
            await ctx.send('And their gone')

    @commands.command(
        name = "softban",
        description = "ban and then unab a user to clean their messages",
        brief = "spam is always fun"
    )
    @commands.guild_only()
    @checks.can_kick()
    async def _softban(self, ctx, user: discord.Member):
        if not await self.will_manage(ctx, user, 'softban'):
            return

        try:
            await user.ban(delete_message_days = 7, reason = 'Softban by {ctx.author}')
            await asyncio.sleep(15)
            await user.unban(reason = f'softban by {ctx.author}')
            await user.send(await ctx.channel.create_invite(max_uses = 1))
        except discord.errors.Forbidden:
            await ctx.send('I dont have the permissions to do that')
        else:
            await ctx.send('their gone now, But i have reinvited them')

    @commands.command(
        name = "clean",
        description = "delete the last x messages from the current chat",
        brief = "just brush it under the rug"
    )
    @commands.guild_only()
    @checks.manage_messages()
    async def _clean(self, ctx, amount: int = 5):
        if not 5 <= amount <= 100:
            return await ctx.send('Amount must be between 5 and 100')

        try:
            await ctx.channel.purge(limit = amount)
        except discord.errors.Forbidden:
            await ctx.send('I dont have the permissions to delete messages')
        else:
            await ctx.send(f'{amount} messages have been purged')

    @commands.command(
        name = "massnick",
        description = "set the nicknames for everyone on the server to same thing",
        brief = "we are legion"
    )
    @commands.guild_only()
    @checks.manage_nicknames()
    async def _massnick(self, ctx, *, nickname: str = None):
        if not nickname is None:
            if not 2 <= len(nickname) <= 32:
                return await ctx.send('Nickname length must be between 2 and 32 characters')
            await ctx.send(f'Setting all nicknames to {nickname}')
        else:
            await ctx.send('Resetting nicknames')

        a = 0

        for member in ctx.guild.members:
            try:
                await member.edit(nick = nickname)
                a+=1
            except discord.errors.Forbidden:
                pass

        await ctx.send(f'massnicked {a} users')

    async def on_member_remove(self, member):
        channelid = self.leave_channels.get(str(member.guild.id), None)
        if channelid is None:
            return
        for each in member.guild.channels:
            if each.id == channelid:
                await each.send(f'{member.mention} just left')

    @commands.command(name = "setleave")
    @commands.guild_only()
    @checks.is_admin()
    async def _setleave(self, ctx, channel: discord.TextChannel = None):
        self.leave_channels[str(ctx.guild.id)] = getattr(channel, 'id', None)
        if channel is None:
            return await ctx.send('cleared the leave channel')
        await ctx.send(f'set leave channel to ``{channel.name}``')

    @_setleave.after_invoke
    async def _after_leave(self, _):
        json.dump(self.leave_channels, open('cogs/store/leave.json', 'w'), indent = 4)

    @commands.group(invoke_without_command = True)
    @commands.guild_only()
    @checks.is_admin()
    async def autorole(self, ctx):
        for (server, roles) in self.autorole_list.items():
            if int(server) == ctx.guild.id:
                if not roles:
                    return await ctx.send('this server has no autoroles')

                embed = quick_embed(ctx, title = 'all autoroles')

                for role in roles:
                    r = discord.utils.get(ctx.guild.roles, id = role)
                    if r is not None:
                        embed.add_field(name = r.name, value = r.id)

                return await ctx.send(embed = embed)

    @autorole.command(
        name = "add",
        description = "add a role to the autorole list",
        brief = "default roles"
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _autorole_add(self, ctx, role: discord.Role):
        for (server, roles) in self.autorole_list.items():
            if int(server) == ctx.guild.id:
                if role.id in roles:
                    return await ctx.send('that role has already been added')
                roles.append(role.id)
                return await ctx.send(f'added ``{role.name}`` to the autorole list')

    @autorole.command(
        name = "remove",
        description = "remove a role from the autorole list",
        brief = "remove a role"
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _autorole_remove(self, ctx, role: discord.Role):
        for (server, roles) in self.autorole_list.items():
            if int(server) == ctx.guild.id:
                if role.id not in roles:
                    return await ctx.send('that role is not an autorole')
                roles.remove(role.id)
                return await ctx.send(f'removed ``{role.name}`` from the autorole list')

    @autorole.before_invoke
    async def _autorole_before(self, ctx):
        for server in self.autorole_list:
            if int(server) == ctx.guild.id:
                return
        self.autorole_list[str(ctx.guild.id)] = []

    @autorole.after_invoke
    async def _autorole_after(self, _):
        json.dump(self.autorole_list, open('cogs/store/autorole.json', 'w'), indent = 4)

    async def on_member_join(self, user):
        for (server, roles) in self.autorole_list.items():
            if int(server) == user.guild.id:
                if not roles:
                    return
                to_add = []
                for role in roles:

                    for each in user.guild.roles:
                        if each.id == role:#but why not use discord.utils.get
                            r = each #because it didnt fucking work, thats why
                            break
                        r = None

                    if r is None:
                        continue
                    to_add.append(r)

                if not to_add:
                    return

                try:
                    return await user.edit(roles = to_add, reason = 'autorole')
                except discord.errors.Forbidden:
                    return

    async def __global_check(self, ctx):
        try:#TODO make this pretty
            for (server, users) in self.server_blacklists.data.items():
                if int(server) == ctx.guild.id:
                    if ctx.author.id in users:
                        await ctx.send('an admin has stopped you from using commands')
                        return False
                    return True
            return True
        except AttributeError:
            return True

    @commands.group(invoke_without_command = True)
    @commands.guild_only()
    async def blacklist(self, ctx):
        for (server, users) in self.server_blacklists.data.items():
            if int(server) == ctx.guild.id:
                if not users:
                    return await ctx.send('this server has no blacklisted users')
                u = []
                for us in users:
                    if us is None:
                        continue
                    usr = self.bot.get_user(us)
                    u.append(usr.name)
                ret = ',\n'.join(u)
                if len(ret) > 1500:
                    ret = [ret[i:i + 1500] for i in range(0, len(ret), 1500)]
                    for part in ret:
                        await ctx.send(f'```css\n{part}```')
                    return await ctx.send('all users sent, maybe you have too many blocked for your own good')
                return await ctx.send(f'```css\n{ret}```')

    @blacklist.command(name = "add")
    @commands.guild_only()
    @checks.is_admin()
    async def _blacklist_add(self, ctx, user: discord.Member):
        for (server, users) in self.server_blacklists.data.items():
            if int(server) == ctx.guild.id:
                if user.id in users:
                    return await ctx.send('that user is already in the blacklist')
                if user.id == ctx.author.id:
                    return await ctx.send('cant block yourself')
                if user.id == self.bot.user.id:
                    return await ctx.send('can you donteth')
                users.append(user.id)
                return await ctx.send(f'added ``{user.name}`` to the blacklist')

    @blacklist.command(name = "remove")
    @commands.guild_only()
    @checks.is_admin()
    async def _blacklist_remove(self, ctx, user: discord.Member):
        for (server, users) in self.server_blacklists.data.items():
            if int(server) == ctx.guild.id:
                if user.id not in users:
                    return await ctx.send(f'``{user.name}`` isnt blacklisted')
                users.remove(user.id)
                return await ctx.send(f'removed ``{user.name}`` from the blacklist')

    @blacklist.before_invoke
    async def _blacklist_before(self, ctx):
        if str(ctx.guild.id) in self.server_blacklists.data.keys():
            return
        self.server_blacklists.data[str(ctx.guild.id)] = []

    @blacklist.after_invoke
    @_blacklist_add.after_invoke
    @_blacklist_remove.after_invoke
    async def _blacklist_after(self, _):
        self.server_blacklists.save()

    @commands.group(invoke_without_command = True)
    async def command(self, ctx):
        pass

    @command.command(name = "lock")
    @checks.is_admin()
    async def _command_lock(self, ctx, name: str):
        if name.lower() not in self.command_blacklist[str(ctx.guild.id)]:
            self.command_blacklist[str(ctx.guild.id)].append(name.lower())
            await ctx.send(f'locked the command {name}')
        else:
            await ctx.send(f'the command {name} is already locked')

    @command.command(name = "unlock")
    @checks.is_admin()
    async def _command_unlock(self, ctx, name: str):
        try:
            self.command_blacklist[str(ctx.guild.id)].remove(name.lower())
            await ctx.send(f'unlocked the command {name}')
        except KeyError:
            await ctx.send(f'the command {name} was never locked')

    async def __global_check(self, ctx):
        if await can_override(ctx):
            return True
        if ctx.invoked_with.lower() in self.command_blacklist.get(str(ctx.guild.id), []):
            await ctx.send('That command has been locked on this server')
            return False
        return True

    @command.before_invoke
    @_command_lock.before_invoke
    @_command_unlock.before_invoke
    async def _command_before(self, ctx):
        try:
            self.command_blacklist[str(ctx.guild.id)]
        except KeyError:
            self.command_blacklist[str(ctx.guild.id)] = []

    @_command_lock.after_invoke
    @_command_unlock.after_invoke
    async def _command_after(self, _):
        json.dump(self.command_blacklist, open('cogs/store/command_blacklist.json', 'w'), indent = 4)

def setup(bot):
    bot.add_cog(Admin(bot))
