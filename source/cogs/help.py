from discord.ext import commands
from .store import quick_embed

class Help:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        print('cog {} loaded'.format(self.__class__.__name__))

    @commands.command(name = "help")
    async def _help(self, ctx, *, name: str = None):
        if name is None:
            await ctx.send(embed = self.__all(ctx))

        elif name in ctx.bot.cogs:
            await ctx.send(embed = self.__cog(ctx, name))

        elif name in ctx.bot.all_commands:
            await ctx.send(embed = self.__command(ctx, name))

        else:
            await ctx.send('No cog or command found called {}'.format(name))

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
        cog = ctx.bot.get_cog(name)

        try: description = cog.description
        except AttributeError: description = 'No description'

        embed = quick_embed(ctx, title = 'All subcommands in {}'.format(name),
        description = description)

        for command in ctx.bot.get_cog_commands(name):
            if not command.hidden:
                try: embed.add_field(name=command.name, value=command.brief)
                except AttributeError: embed.add_field(name=command.name, value='No description')

        return embed

    @classmethod
    def __command(self, ctx, name: str):
        command = ctx.bot.all_commands.get(name)

        try: description = command.description
        except AttributeError: description = 'None'

        if description == '':
            description = None

        try: usage = command.usage
        except AttributeError: usage = command.signature

        if usage is None:
            usage = command.signature

        try: aliases = commands.aliases
        except AttributeError: aliases = ['None']

        embed = quick_embed(ctx, title = command.name, description = 'Inside cog: {}'.format(command.cog_name))
        embed.add_field(name = 'Description', value = description)

        try: embed.add_field(name = 'Aliases', value = ', '.join(aliases))
        except TypeError: pass

        embed.add_field(name = 'Usage', value = usage)
        return embed

def setup(bot):
    bot.add_cog(Help(bot))