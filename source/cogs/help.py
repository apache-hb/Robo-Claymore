from itertools import chain

import discord
from discord.ext import commands
from fuzzywuzzy import process

from .utils.shortcuts import quick_embed
from .utils.saved_dict import SavedDict

class Help:
    def __init__(self, bot):
        self.bot = bot
        self.complaints = SavedDict('cogs/store/complaints.json', content = '[]')
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

        for name, cog in ctx.bot.cogs.items():
            emb = quick_embed(ctx, title = name)
            ret = ''
            for command in cog:
                if getattr(ctx.bot.get_cog(cog), 'hidden', False):
                    continue

                if not getattr(command, 'hidden', False):
                    ret += command.name + '\n'

            emb.add_field(name = cog, value = ret, inline = False)

            if not getattr(ctx.bot.get_cog(cog), 'hidden', False):
                await ctx.author.send(embed = emb)

    def __all(self, ctx):
        ret = '\n'.join([name for name, cog in self.bot.cogs.items() if not getattr(cog, 'hidden', False)])

        return quick_embed(
            ctx,
            title = f'All commands for {ctx.bot.user.name}'
        ).add_field(name = 'All cogs', value = ret)

    def __cog(self, ctx, name: str):
        cog = self.__get_cog(name)

        if cog is None:
            return quick_embed(ctx, f'No command called {name} found')

        embed = quick_embed(
            ctx,
            title = f'All subcommands in {name}',
            description = getattr(cog, 'description', 'No description')
        )

        for command in ctx.bot.get_cog_commands(cog.__class__.__name__):
            if not command.hidden:
                embed.add_field(name = command.name, value = getattr(command, 'brief', 'No description'), inline = False)

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
        embed.add_field(name = 'Description', value = getattr(command, 'description', 'None') or 'None')
        embed.add_field(name = 'Aliases', value = ', '.join(getattr(command, 'aliases', ['None'])) or 'None')
        embed.add_field(name = 'Brief', value = getattr(command, 'brief', 'None') or 'None')
        embed.add_field(name = 'Usage', value = command.signature)
        embed.add_field(name = 'Detailed usage', value = command.callback.__doc__)

        return embed

    @commands.command(name = "complain")
    async def _complain(self, ctx, *, msg: str):
        self.complaints.data.append({
            'name': ctx.author.name,
            'id': ctx.author.id,
            'message': msg
        })
        self.complaints.save()
        await ctx.send('your complaint has been submitted')

def setup(bot):
    bot.remove_command('help')
    print('Removed the default help command')
    bot.add_cog(Help(bot))
