from itertools import chain

import discord
from discord.ext import commands
from fuzzywuzzy import process

from .utils.shortcuts import quick_embed

class Help:
    def __init__(self, bot):
        self.bot = bot
        print(f'cog {self.__class__.__name__} loaded')

    def __get_cog(self, name: str):
        for (key, val) in self.bot.cogs.items():
            if key.lower() == name.lower():
                return val
        return None

    async def __get_fuzzy(self, ctx, name: str):
        ret = quick_embed(ctx, 'Reccomended commands & cogs')
        fuzzed = process.extract(name, chain(self.bot.all_commands, self.bot.cogs.keys()), limit = 3)

        for pair in fuzzed:
            ret.add_field(name = pair[0], value = f'{pair[1]}% chance this is what you wanted')

        await ctx.send(embed = ret)

    @commands.command(
        name = "help",
        description = 'get help for a cog or command as well as a description and usage',
        brief = 'get help'
    )
    async def _help(self, ctx, *, name: str = None):
        if name is None:
            await ctx.send(embed = self.__all(ctx))
        elif self.__get_cog(name) is not None:
            await ctx.send(embed = self.__cog(ctx, name.lower()))
        elif name.lower() in ctx.bot.all_commands:
            await ctx.send(embed = self.__command(ctx, name.lower()))
        else:
            await self.__get_fuzzy(ctx, name)

    @commands.command(
        name = 'allcommands',
        description = 'get a list of all commands the bot has available',
        breif = 'list all commands'
    )
    async def _all_commands(self, ctx):
        embed = quick_embed(ctx, title = 'All cogs and commands', description = f'{len(self.bot.all_commands)} commands total')

        await ctx.author.send(embed = embed)

        for cog in ctx.bot.cogs:
            emb = quick_embed(ctx, title = ctx.bot.get_cog(cog).__class__.__name__)
            ret = ''
            for command in ctx.bot.get_cog_commands(cog):
                if getattr(ctx.bot.get_cog(cog), 'hidden', False):
                    continue

                if not getattr(command, 'hidden', False):
                    ret += command.name + '\n'

            emb.add_field(name = cog, value = ret, inline = False)

            if not getattr(ctx.bot.get_cog(cog), 'hidden', False):
                await ctx.author.send(embed = emb)

    def __all(self, ctx):
        ret = ''
        for cog in self.bot.cogs:
            cmd = self.bot.get_cog(cog)
            try:
                if not cmd.hidden:
                    ret += cog + '\n'
            except AttributeError:
                ret += cog + '\n'

        embed = quick_embed(ctx, title = f'All commands for {ctx.bot.user.name}')
        embed.add_field(name = 'All cogs', value = ret)

        return embed

    def __cog(self, ctx, name: str):
        cog = self.__get_cog(name)

        if cog is None:
            return quick_embed(ctx, f'No command called {name} found')

        try:
            description = cog.description
        except AttributeError:
            description = 'No description'

        embed = quick_embed(ctx, title = f'All subcommands in {name}',
        description = description)

        for command in ctx.bot.get_cog_commands(cog.__class__.__name__):
            if not command.hidden:
                try:
                    embed.add_field(name=command.name, value=command.brief, inline = False)
                except AttributeError:
                    embed.add_field(name=command.name, value='No description', inline = False)

        return embed

    def group_embed(self, ctx, name: str) -> discord.Embed:
        group = self.bot.all_commands.get(name)

        embed = quick_embed(ctx, f'All subcommands for group {name}')

        for command in group.walk_commands():
            embed.add_field(
                name = command.name,
                value = f'''
Description: {command.description}
Usage: {command.usage}
Aliases: {command.aliases}'''
            )

        return embed

    def __command(self, ctx, name: str) -> discord.Embed:
        command = self.bot.all_commands.get(name)

        if isinstance(command, discord.ext.commands.core.Group):
            return self.group_embed(ctx, name)

        embed = quick_embed(ctx, title = command.name, description = f'Inside cog {command.cog_name}')

        try:
            description = command.description
        except AttributeError:
            description = 'None'

        if not description:
            description = 'None'

        embed.add_field(name = 'Description', value = description)

        try:
            aliases = ', '.join(command.aliases)
        except AttributeError:
            aliases = 'None'

        if not aliases:
            aliases = 'None'

        embed.add_field(name = 'Aliases', value = aliases)

        try:
            brief = command.brief
        except AttributeError:
            brief = 'None'
        if not brief:
            brief = 'None'

        embed.add_field(name = 'Brief', value = brief)

        embed.add_field(name = 'Usage', value = command.signature)

        return embed

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
