import asyncio
import json

import discord
from discord.ext import commands

from .utils.networking import hastebin
from .utils.checks import can_override
from .utils.shortcuts import quick_embed, try_file

class Owner:
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(try_file('cogs/store/config.json'))
        self.spam = True
        self.hidden = True
        self.bully = []
        print('cog {} loaded'.format(self.__class__.__name__))

    async def __local_check(self, ctx):
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

    @commands.command(name = "test")
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
        self.spam = False
        ret = await ctx.send('Stopping spam')
        await asyncio.sleep(15)
        self.spam = True
        await ret.edit(content = 'The spam should be over')

    @commands.command(name = "ping")
    async def _ping(self, ctx):
        ret = '%.{}f'.format(3) % ctx.bot.latency
        await ctx.send('{} seconds latency to discord'.format(ret))

    @commands.command(name = "massdm")
    async def _massdm(self, ctx, count: int = 0, *, message: str = 'My name jeff'):
        await ctx.send(f'the crime against humanity has begun for {count + 1} cycles')

        for _ in range(count):
            if self.spam:
                for user in ctx.guilds.members:
                    try:
                        await user.send(message)
                    except discord.errors.Forbidden:
                        pass
            else:
                return await ctx.send('The spam has been inturrupted')

    @commands.command(name = "massprod")
    async def _massprod(self, ctx):
        for user in ctx.guild.members:
            await ctx.send(user.mention, delete_after = .5)

    @commands.command(name = "prod")
    async def _prod(self, ctx, user: discord.Member, count: int = 10, *, message: str = 'Skidaddle skidoodle'):
        await ctx.send(f'The spam against {user.name} has begun for {count} cycles')

        for _ in range(count):
            if self.spam:
                try:
                    await user.send(message)
                except discord.errors.Forbidden:
                    return await ctx.send('They blocked me')
            else:
                return await ctx.send('The spam has been inturrupted')

    @commands.command(name = "userlist")
    async def _userlist(self, ctx):
        ret = ''
        for user in ctx.guild.members:
            ret += ' '+user.mention
        await ctx.send(await hastebin(content = ret))

    #TODO: whitelist managing

    @commands.group(invoke_without_command = True)
    async def whitelist(self, ctx):
        if not whitelist:
            return await ctx.send('No users have been whitelisted yet')

        embed = quick_embed(ctx, title = "all whitelisted users")


        for identifier in whitelist:
            user = await ctx.bot.get_user_info(identifier)
            embed.add_field(name = user.name, value = user.id)

        await ctx.send(embed = embed)

    @whitelist.command(name = "add")
    async def _whitelist_add(self, ctx, user: discord.Member):
        if not user.id in whitelist:
            whitelist.append(user.id)
            return await ctx.send(f'{user.name} was added to the whitelist')

        await ctx.send(f'{user.name} is already on the whitelist')

    @whitelist.command(name = "remove")
    async def _whitelist_remove(self, ctx, user: discord.Member):
        try:
            whitelist.remove(user.id)
        except ValueError:
            return await ctx.send(f'{user.name} is not in the whitelist')

        await ctx.send(f'{user.name} was removed from the whitelist')

    @whitelist.command(name = "purge")
    async def _whitelist_purge(self, ctx):
        await ctx.send('Whitelist was purged')

    @_whitelist_add.after_invoke
    @_whitelist_purge.after_invoke
    @_whitelist_remove.after_invoke
    async def _whitelist_after(self, _):
        json.dump(whitelist, open('cogs/store/whitelist.json', 'w'), indent = 4)

    #TODO: blacklist managing

    @commands.group(invoke_without_command = True)
    async def blacklist(self, ctx):
        pass

    @blacklist.command(name = "add")
    async def _blacklist_add(self, ctx, user: discord.Member):
        pass

    @blacklist.command(name = "remove")
    async def _blacklist_remove(self, ctx, user: discord.Member):
        pass

    @blacklist.command(name = "purge")
    async def _blacklist_purge(self, ctx):
        pass

    @_blacklist_add.after_invoke
    @_blacklist_remove.after_invoke
    @_blacklist_purge.after_invoke
    async def _blacklist_after(self, _):
        pass
        #json.dump(blacklist, open('cogs/store/blacklist.json', 'w'), indent = 4)

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

    @cogs.command(name = "enable")
    async def _cogs_enable(self, ctx, name: str):
        if ctx.bot.get_cog(name.lower()) is None:
            return await ctx.send(f'{name} is not a cog')

        if not name.lower() in config['disabled']['cogs']:
            return await ctx.send('That cog isn\'t disabled')

        config['disabled']['cogs'].remove(name.lower())
        json.dump(config, open('cogs/store/config.json', 'w'), indent = 4)

    @cogs.command(name = "disable")
    async def _cogs_disable(self, ctx, name: str):
        if ctx.bot.get_cog(name.lower()) is None:
            return await ctx.send(f'{name} is not a cog')

        if name.lower() in config['disabled']['cogs']:
            return await ctx.send('That cog is already disabled')

        config['disabled']['cogs'].append(name.lower())
        json.dump(config, open('cogs/store/config.json', 'w'), indent = 4)


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
        for channel in guild.text_channels[:25]:
            ret += '{0.name}#{0.id}\n'.format(channel)
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
                continue
            embed.add_field(name = perm, value = getattr(perms, perm))

        await ctx.send(embed = embed)

    @remote.command(name = "channelinfo")
    async def _remote_channelinfo(self, ctx, channel: int):
        target = ctx.bot.get_channel(channel)

        if target is None:
            return await ctx.send(f'No channel with an id of {channel} found')

        ret = '{}#{}\n'.format(target.name, target.id)
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
