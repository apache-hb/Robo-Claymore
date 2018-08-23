import asyncio
import json

import discord
from discord.ext import commands

from .utils.checks import can_override
from .utils.networking import hastebin
from .utils.shortcuts import quick_embed, try_file

class Owner:
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(try_file('cogs/store/config.json'))

        self.blocklist = json.load(try_file('cogs/store/blacklist.json'))

        #This replaces the spam bool as it allows ofr much cleaner and more reliable
        #killing of function execution
        #thanks to PikalaxALT#5823 for help with this
        self.futures = {}

        self.hidden = True
        self.bully = []
        #TODO move stuff like the config to external file to be global
        #TODO whitelist, blacklist and related checks
        print(f'cog {self.__class__.__name__} loaded')

    async def __local_check(self, ctx):
        print('{0.author.name} tried to use {0.invoked_with}'.format(ctx))

        if await can_override(ctx):
            return True
        await ctx.send('go away')
        return False

    async def on_member_update(self, before, after):
        if before.display_name == after.display_name:
            return

        if not self.bully:
            return

        for user in self.bully:
            if user['id'] == before.id:
                try:
                    await before.edit(nick = user['name'])
                except discord.errors.Forbidden:
                    pass

    @commands.group(name = "test")
    async def _test(self, ctx):
        return await ctx.message.add_reaction('🇧')

    @commands.command(name = "eval")
    async def _eval(self, ctx, *, text: str):
        try:
            await ctx.send(eval(text))
        except Exception as e:
            await ctx.send(e)

    @commands.command(name = "echo")
    async def _echo(self, ctx, *, text: str):
        await ctx.send(text)

    #TODO make this nicer to use and easier to read/write
    @commands.group(invoke_without_command = False, name = "bully")
    async def _bully(self, ctx):
        pass

    @_bully.command(name = "start")
    async def _bully_start(self, ctx, user: discord.Member, *, name: str):
        ret = {
            'user': user.id,
            'name': name
        }

        if not ctx.bot.permissions_in(ctx.channel).manage_nicknames:
            return await ctx.send('I cant bully them')

        self.bully.append(ret)

        await user.edit(nick = name)
        await ctx.send(f'Now bullying {user.name}')

    @_bully.command(name = "stop")
    async def _bully_stop(self, ctx, user: discord.Member):
        for item in bully[:]:
            if item['user'] == user.id:
                bully.remove(item)
                return await ctx.send(f'i have stopped bullying {user.name}')
        await ctx.send(f'I was never bullying {user.name}')

    #this command just changes a bool and waits, its used to stop spamming without restarting the bot
    @commands.command(name = "panic")
    async def _panic(self, ctx):
        r = await ctx.send('stopping spam')
        for (_, future) in self.futures.items():
            future.cancel()
        self.futures.clear()
        await r.edit(content = 'spam should be over now')

    @commands.command(name = "ping")
    async def _ping(self, ctx):
        await ctx.send('%.3f seconds latency to discord' % ctx.bot.latency)

    async def do_massdm(self, ctx, count: int, message: str):
        await ctx.send(f'the crime against humanity has begun for {count + 1} cycles')

        for _ in range(count):
            for user in ctx.guilds.members:
                try:
                    await user.send(message)
                except discord.errors.Forbidden:
                    pass

    @commands.command(name = "massdm")
    async def _massdm(self, ctx, count: int = 0, *, message: str = 'My name jeff'):
        future = self.do_massdm(ctx, count, message)
        self.futures[ctx.message.id] = asyncio.ensure_future(future)
        try:
            await asyncio.wait_for(future, timeout = 9999)
        except RuntimeError:
            return await ctx.send('command was cancelled/ended')

    @commands.command(name = "massprod")
    async def _massprod(self, ctx):
        for user in ctx.guild.members:
            await ctx.send(user.mention, delete_after = .5)

    async def do_prod(self, ctx, user: discord.Member, count: int, message: str):
        await ctx.send(f'The spam against {user.mention} has begun for {count} cycles')

        for _ in range(count):
            try:
                await user.send(message)
            except discord.errors.Forbidden:
                return await ctx.send(f'{user.mention} blocked me')

    @commands.command(name = "prod")
    async def _prod(self, ctx, user: discord.Member, count: int = 10, *, message: str = 'Skidaddle skidoodle'):
        future = self.do_prod(ctx, user, count, message)
        self.futures[ctx.message.id] = asyncio.ensure_future(future)
        try:
            await asyncio.wait_for(future, timeout = 999999)
        except RuntimeError:
            return await ctx.send('command was cancelled/ended')

    @commands.command(name = "userlist")
    async def _userlist(self, ctx):
        ret = ''
        for user in ctx.guild.members:
            ret += ' ' + user.mention
        await ctx.send(await hastebin(content = ret))

    async def __global_check(self, ctx):
        if ctx.author.id in self.blocklist:
            await ctx.send('eat pant')
            return False
        return True

    @commands.group(invoke_without_command = True)
    async def block(self, ctx):
        if not self.blocklist:
            return await ctx.send('no one is blocked')
        embed = quick_embed(ctx, title = 'all blocked users')
        for user in self.blocklist:
            u = self.bot.get_user(user)
            embed.add_field(name = u, value = u.id)
        await ctx.send(embed = embed)


    @block.command(name = "add")
    async def _block_add(self, ctx, user: discord.User):
        if user.id not in self.blocklist:
            self.blocklist.append(user.id)
            return await ctx.send(f'added ``{user.name}`` to the blocklist')
        await ctx.send(f'``{user.name}`` is already blocked')

    @block.command(name = "remove")
    async def _block_remove(self, ctx, user: discord.User):
        if user.id in self.blocklist:
            self.blocklist.remove(user.id)
            return await ctx.send(f'removed ``{user.name}`` from the blocklist')
        await ctx.send(f'``{user.name}`` isnt blocked')

    @commands.group(name = "cogs", invoke_without_command = True)
    async def cogs(self, ctx):
        ret = ''

        for cog in ctx.bot.cogs:
            ret += cog + '\n'

        embed = quick_embed(ctx, title = 'All cogs currently registered',
        description = 'Disable and enable them with subcommands')
        embed.add_field(name = 'Currently loaded', value = ret)

        return await ctx.send(embed = embed)

    @cogs.command(name = "load")
    async def _cogs_load(self, ctx, name: str):
        try:
            self.bot.load_extension('cogs.' + name.lower())
        except Exception as e:
            return await ctx.send(e)
        return await ctx.send(f'Cog {name} loaded correctly')

    @cogs.command(name = "unload")
    async def _cogs_unload(self, ctx, name: str):
        try:
            self.bot.unload_extension('cogs.' + name.lower())
        except Exception as e:
            return await ctx.send(e)
        return await ctx.send(f'Cog {name} unloaded')

    @cogs.command(name = "reload")
    async def _cogs_reload(self, ctx, name: str):
        try:
            self.bot.unload_extension('cogs.' + name.lower())
            self.bot.load_extension('cogs.' + name.lower())
        except Exception as e:
            return await ctx.send(e)
        return await ctx.send(f'Cog {name} reloaded correctly')

    @commands.group(invoke_without_command = True)
    async def remote(self, ctx):
        pass

    @remote.command(name = "userlist")
    async def _remote_userlist(self, ctx, guild: int):
        ret = ''
        server = ctx.bot.get_guild(guild)

        if server is None:
            return await ctx.send(f'I am not in a server with an id of {guild}')

        for user in server.members:
            ret += ' '+user.mention
        await ctx.send(await hastebin(content = ret))

    @remote.command(name = "userinfo")
    async def _remote_userinfo(self, ctx, user: int):
        try:
            ret = await ctx.bot.get_user_info(user)
        except discord.errors.NotFound:
            return await ctx.send('No user with that id found')

        embed = quick_embed(ctx, title = 'User information')
        embed.add_field(name = 'Username', value = '{0.name}#{0.discriminator}'.format(ret))
        embed.set_thumbnail(url = ret.avatar_url)
        embed.add_field(name = 'Created at', value = ret.created_at)

        await ctx.send(embed = embed)

    @remote.command(name = "serverinfo")
    async def _remote_serverinfo(self, ctx, server: int):
        guild = ctx.bot.get_guild(server)

        if guild is None:
            return await ctx.send(f'No server with an id of {server} found')

        ret = f'```\n{guild.name}\n'
        for channel in guild.text_channels[:25]:#only send the first 25 channels in the server
            ret += '{0.name}#{0.id}\n'.format(channel)#TODO class them under categorys if there are any
        ret += '```'

        await ctx.send(ret)

    @remote.command(name = "botperms")
    async def _remote_botperms(self, ctx, channel: int):
        guild_channel = ctx.bot.get_channel(channel)

        if guild_channel is None:
            return await ctx.send(f'No channel with an id of {channel} found')

        embed = quick_embed(ctx, "bot permissions")

        bot_relation = discord.utils.get(guild_channel.guild.members, id = ctx.bot.user.id)

        perms = guild_channel.permissions_for(bot_relation)

        for perm in dir(perms):
            if perm.startswith('__') or callable(getattr(perms, perm)):
                continue#TODO extract to function (maybe `all_attrs(obj)`)
            embed.add_field(name = perm, value = getattr(perms, perm))

        await ctx.send(embed = embed)

    @remote.command(name = "channelinfo")
    async def _remote_channelinfo(self, ctx, channel: int, create_invite: bool = False):
        target = ctx.bot.get_channel(channel)

        if target is None:
            return await ctx.send(f'No channel with an id of {channel} found')

        ret = '{}#{}\n'.format(target.name, target.id)

        if create_invite:
            try:
                ret += str(await target.create_invite())
            except Exception:
                ret += 'I cant make an invite for this channel\n'

        await ctx.send(ret)

    @remote.command(name = "channelhistory")
    async def _remote_channelhistory(self, ctx, channel: int):
        target = ctx.bot.get_channel(channel)

        if target is None:
            return await ctx.send('No channel found')

        ret = 'Messages in {0.name}#{0.id}\n'.format(target)

        async for message in target.history():
            ret += '{0.author.name}: {0.content}\n'.format(message)

        await ctx.send(await hastebin(ret))

    @remote.command(name = "sendmessage")
    async def _remote_sendmessage(self, ctx, channel: int, *, message: str):
        target = ctx.bot.get_channel(channel)

        if target is None:
            return await ctx.send('No channel found')

        try:
            await target.send(message)
        except Exception:
            return await ctx.send('I cannot send messages to that channel')

        await ctx.send('message sent')

def setup(bot):
    bot.add_cog(Owner(bot))
