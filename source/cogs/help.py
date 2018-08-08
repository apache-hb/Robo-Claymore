from discord.ext import commands
from .store import quick_embed
import discord
from fuzzywuzzy import process
from itertools import chain

class Help:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        print('cog {} loaded'.format(self.__class__.__name__))

    @classmethod
    def __get_cog(self, ctx, name: str):
        for key, val in ctx.bot.cogs.items():
            if key.lower() == name.lower():
                return val
        return None

    @classmethod
    async def __get_fuzzy(self, ctx, name: str):
        ret = quick_embed(ctx, 'Reccomended commands & cogs')
        fuzzed = process.extract(name, chain(ctx.bot.all_commands, ctx.bot.cogs.keys()), limit = 3)

        for pair in fuzzed:
            ret.add_field(name = pair[0], value = '{}% chance this is what you wanted'.format(str(pair[1])))

        await ctx.send(embed = ret)


    @commands.command(name = "help")
    async def _help(self, ctx, *, name: str = None):
        if name is None:
            await ctx.send(embed = self.__all(ctx))

        elif self.__get_cog(ctx, name) is not None:
            await ctx.send(embed = self.__cog(ctx, name.lower()))
        elif name.lower() in ctx.bot.all_commands:
            await ctx.send(embed = self.__command(ctx, name.lower()))
        else:
            await self.__get_fuzzy(ctx, name)

    @commands.command(name = 'allcommands')
    async def _all_commands(self, ctx):
        embed = quick_embed(ctx, title = 'All cogs and commands')

        for cog in ctx.bot.cogs:
            ret = ''
            for command in ctx.bot.get_cog_commands(cog):
                try:#if the cog is hidden, skip it
                    if ctx.bot.get_cog(cog).hidden: continue
                except AttributeError: pass
                try:
                    if not command.hidden:
                        ret += command.name + '\n'
                except AttributeError:
                    ret += command.name + '\n'

            try:#if the command is hidden, dont add an empty body
                if not ctx.bot.get_cog(cog).hidden:
                    embed.add_field(name = cog, value = ret, inline = False)
            except AttributeError: pass

        await ctx.author.send(embed = embed)

    @classmethod
    def __all(self, ctx):
        ret = ''
        for cog in ctx.bot.cogs:
            cmd = ctx.bot.get_cog(cog)
            try:
                if not cmd.hidden:
                    ret += cog + '\n'
            except AttributeError:
                ret += cog + '\n'

        embed = quick_embed(ctx, title = 'All commands for {}'.format(ctx.bot.user.name))
        embed.add_field(name = 'All cogs', value = ret)

        return embed

    @classmethod
    def __cog(self, ctx, name: str):
        cog = self.__get_cog(ctx, name)

        if cog is None:
            return quick_embed(ctx, 'No command called {} found'.format(name))

        try: description = cog.description
        except AttributeError: description = 'No description'

        embed = quick_embed(ctx, title = 'All subcommands in {}'.format(name),
        description = description)

        for command in ctx.bot.get_cog_commands(cog.__class__.__name__):
            if not command.hidden:
                try: embed.add_field(name=command.name, value=command.brief)
                except AttributeError: embed.add_field(name=command.name, value='No description')

        return embed

    @classmethod
    def group_embed(self, ctx, name: str) -> discord.Embed:
        group = ctx.bot.all_commands.get(name)

        embed = quick_embed(ctx, 'All subcommands for group {}'.format(name))

        for command in group.walk_commands():
            embed.add_field(name = command.name,
                value = 'Description: {0.description}\nUsage: {0.usage}\nAliases: {0.aliases}'.format(command)
            )

        return embed

    @classmethod
    def __command(self, ctx, name: str) -> discord.Embed:
        command = ctx.bot.all_commands.get(name)

        if isinstance(command, discord.ext.commands.core.Group):
            return self.group_embed(ctx, name)

        embed = quick_embed(ctx, title = command.name, description = 'Inside cog {}'.format(command.cog_name))

        try: description = command.description
        except: description = 'None'

        if description == '':
            description = 'None'

        embed.add_field(name = 'Description', value = description)

        try: aliases = ', '.join(command.aliases)
        except: aliases = 'None'

        if aliases == '':
            aliases = 'None'

        embed.add_field(name = 'Aliases', value = aliases)

        try: usage = command.usage
        except: usage = name

        embed.add_field(name = 'Usage', value = usage)

        return embed

def setup(bot):
    bot.add_cog(Help(bot))