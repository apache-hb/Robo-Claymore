import asyncio
import json
from dis import disassemble

import discord
from discord.ext import commands

from .store import (blacklist, config, hastebin, hastebin_error, quick_embed,
                    whitelist)


class Owner:
    def __init__(self, bot):
        self.bot = bot
        self.spam = True
        self.hidden = True
        print('cog {} loaded'.format(self.__class__.__name__))

    async def __local_check(self, ctx):
        if ctx.author.id == int(config['discord']['owner']) or ctx.author.id in whitelist:
            return True
        await ctx.send('go away')
        return False

    @commands.command(name = "invite")
    async def _invite(self, ctx):
        await ctx.send('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=66321471'.format(self.bot.user.id))

    @commands.command(name = "eval")
    async def _eval(self, ctx, *, text: str):
        try: await ctx.send(eval(text))
        except Exception as e: await ctx.send(e)

    @commands.command(name = "echo")
    async def _echo(self, ctx, *, text: str):
        await ctx.send(text)

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
        await ctx.send('the crime against humanity has begun for {} cycles'.format(count + 1))

        for x in range(count):
            if self.spam:
                for user in ctx.guilds.members:
                    try:
                        await user.send(message)
                    except discord.errors.Forbidden:
                        pass
            else:
                return await ctx.send('The spam has been inturrupted')

    @commands.command(name = "prod")
    async def _prod(self, ctx, user: discord.Member, count: int = 10, *, message: str = 'Skidaddle skidoodle'):
        await ctx.send('The spam against {} has begun for {} cycles'.format(user.name, count))

        for x in range(count):
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

    @commands.group(invoke_without_command = True)
    async def whitelist(self, ctx):
        pass

    @whitelist.command(name = "add")
    async def _whitelist_add(self, ctx, user: discord.Member):
        if not user.id in whitelist:
            whitelist.append(user.id)
            json.dump(whitelist, open('cogs/store/whitelist.json', 'w'), indent = 4)
            return await ctx.send('{} was added to the whitelist'.format(user.name))

        await ctx.send('{} is already on the whitelist'.format(user.name))

    @whitelist.command(name = "remove")
    async def _whitelist_remove(self, ctx, user: discord.Member):
        try:
            whitelist.remove(user.id)
        except ValueError:
            return await ctx.send('{} is not in the whitelist'.format(user.name))

        json.dump(whitelist, open('cogs/store/whitelist.json', 'w'), indent = 4)
        await ctx.send('{} was removed from the whitelist'.format(user.name))


    @whitelist.command(name = "purge")
    async def _whitelist_purge(self, ctx):
        whitelist = []
        json.dump(whitelist, open('cogs/store/whitelist.json', 'w'), indent = 4)
        await ctx.send('Whitelist was purged')

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
        return await ctx.send('Cog {} loaded correctly'.format(name))

    @cogs.command(name = "unload")
    async def _cogs_unload(self, ctx, name: str):
        try:
            self.bot.unload_extension('cogs.' + name.lower())
        except Exception as e:
            return await ctx.send(e)
        return await ctx.send('Cog {} unloaded'.format(name))

    @cogs.command(name = "reload")
    async def _cogs_reload(self, ctx, name: str):
        try:
            self.bot.unload_extension('cogs.' + name.lower())
            self.bot.load_extension('cogs.' + name.lower())
        except Exception as e:
            return await ctx.send(e)
        return await ctx.send('Cog {} reloaded correctly'.format(name))

    @cogs.command(name = "enable")
    async def _cogs_enable(self, ctx, name: str):
        if ctx.bot.get_cog(name.lower()) is None:
            return await ctx.send('{} is not a cog'.format(name))

        if not name.lower() in config['disabled']['cogs']:
            return await ctx.send('That cog isn\'t disabled')

        config['disabled']['cogs'].remove(name.lower())
        json.dump(config, open('cogs/store/config.json', 'w'), indent = 4)

    @cogs.command(name = "disable")
    async def _cogs_disable(self, ctx, name: str):
        if ctx.bot.get_cog(name.lower()) is None:
            return await ctx.send('{} is not a cog'.format(name))

        if name.lower() in config['disabled']['cogs']:
            return await ctx.send('That cog is already disabled')

        config['disabled']['cogs'].append(name.lower())
        json.dump(config, open('cogs/store/config.json', 'w'), indent = 4)


    @commands.group(invoke_without_command = True)
    async def remote(self, ctx):
        pass

    @remote.command(name = "userinfo")
    async def _remote_userinfo(self, ctx, user: int):
        try:
            ret = await ctx.bot.get_user_info(user)
        except discord.errors.NotFound:
            return await ctx.send('No user with that id found')

        embed = quick_embed(ctx, title = 'User information')
        embed.add_field(name = 'Username', value = '{}#{}'.format(ret.name, ret.discriminator))
        embed.set_thumbnail(url = ret.avatar_url)
        embed.add_field(name = 'Created at', value = ret.created_at)

        await ctx.send(embed = embed)

    @remote.command(name = "serverinfo")
    async def _remote_serverinfo(self, ctx, server: int):
        guild = ctx.bot.get_guild(server)

        if guild is None:
            return await ctx.send('No server with an id of {} found'.format(server))

        ret = '```\n{}\n'.format(guild.name)
        for channel in guild.text_channels[:25]:
            ret += '{}#{}\n'.format(channel.name, channel.id)
        ret += '```'

        await ctx.send(ret)

    @remote.command(name = "channelinfo")
    async def _remote_channelinfo(self, ctx, channel: int):
        target = ctx.bot.get_channel(channel)

        if target is None:
            return await ctx.send('No channel with an id of {} found'.format(channel))

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

        ret = 'Messages in {}#{}\n'.format(target.name, target.id)

        async for message in target.history():
            ret += '{}: {}\n'.format(message.author.name, message.content)

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
