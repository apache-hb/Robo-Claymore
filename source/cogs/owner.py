from discord.ext import commands
import discord
from .store import (whitelist, blacklist,
hastebin, quick_embed, config,
hastebin_error)
import json
import asyncio

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

    @commands.command(name = "panic")
    async def _panic(self, ctx):
        self.spam = False
        ret = await ctx.send('Stopping spam')
        asyncio.sleep(15)
        self.spam = True
        await ret.edit('The spam should be over')

    @commands.command(name = "ping")
    async def _ping(self, ctx):
        ret = '%.{}f'.format(3) % ctx.bot.latency
        await ctx.send('{} seconds latency to discord'.format(ret))


    @commands.command(name = "massdm")
    async def _massdm(self, ctx, count: int = 0, *, message: str = 'My name jeff'):
        for x in range(count):
            if self.spam:
                for user in ctx.guilds.members:
                    await user.send(message)
            else:
                return await ctx.send('The spam has been inturrupted')

    @commands.command(name = "prod")
    async def _prod(self, ctx, user: discord.Member, count: int = 10, *, message: str = 'Skidaddle skidoodle'):
        for x in range(count):
            if self.spam:
                await user.send(message)
            else:
                return await ctx.send('The spam has been inturrupted')

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

def setup(bot):
    bot.add_cog(Owner(bot))