import discord
from discord.ext import commands

from .store import style_embed

class HiddenCog:
    pass

class Help:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Help me!"
    description = "Retrives a list of commands the bot has that the user can access"
    blocked_roles = []
    hidden = False

    async def __local_check(self, ctx):
        if ctx.bot.is_owner(ctx.author.id):
            return True
        return True

    @commands.command(name="help")
    async def _help(self, ctx, command: str=None):
        if command is None:
            await ctx.send(embed=self.full_help(ctx))
        elif command in ctx.bot.cogs:
            await ctx.send(embed=self.cog_help(ctx, command))
        elif command in ctx.bot.all_commands:
            await ctx.send(embed=self.command_help(ctx, command))
        else:
            await ctx.send('No cog or command called {} found'.format(command))

    def command_help(self, ctx, command: str):
        target = ctx.bot.all_commands.get(command)
        aliases = target.aliases

        if hasattr(target, 'description'): 
            description = target.description
            if description =='':
                description = 'None'
        else: 
            description = 'None'

        if hasattr(target, 'usage'): 
            usage = target.usage
        else: 
            usage = 'None'

        if not aliases: 
            aliases = ['None']

        embed = style_embed(ctx, title=target.name, description='Inside cog {}'.format(target.cog_name))
        embed.add_field(name='Description', value=description)
        embed.add_field(name='Aliases', value=', '.join(aliases))
        embed.add_field(name='Usage', value=usage)
        return embed

    def cog_help(self, ctx, cog: str):
        target = ctx.bot.get_cog(cog)
        embed=style_embed(ctx, title='Information and subcommands in {}'.format(cog),
        description=target.description)
        for command in ctx.bot.get_cog_commands(cog):
            if not command.hidden:
                if hasattr(command, 'brief'):
                    embed.add_field(name=command.name, value=command.brief)
                else:
                    embed.add_field(name=command.name, value='None')
        return embed
        
    def full_help(self, ctx):
        ret=''
        for cog in ctx.bot.cogs:
            if hasattr(cog, 'hidden'):
                if not cog.hidden:
                    ret+=cog+'\n'
                    continue
                ret+=cog+'\n'
                continue
            ret+=cog+'\n'
            continue
        embed=style_embed(ctx, title='All cogs for bot {}'.format(ctx.bot.user.name))
        embed.add_field(name='All cogs', value=ret)
        return embed

    @commands.command(name="request")
    async def _request(self, ctx, *, message: str):
        pass

    @commands.command(name="report")
    async def _report(self, ctx, *, message: str):
        pass

def setup(bot):
    bot.add_cog(Help(bot))