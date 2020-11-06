from discord.embeds import Embed
from claymore.utils import wheel, Context
from claymore.claymore import Claymore
from discord.ext.commands import command, CommandNotFound
from discord.user import User
from fuzzywuzzy import process as fuzz
from traceback import format_exception
from textwrap import dedent

def first(iter, key):
    for k, v in iter:
        if k.lower() == key:
            return v
    
    return None

def fuzzy(items, term, cutoff = 50):
    return [ pair[0] for pair in fuzz.extract(term, items, limit = 3) if pair[1] > cutoff]

class Help(wheel(desc = 'bot usage commands')):
    def __init__(self, bot: Claymore):
        super().__init__(bot)
        bot.add_listener(self.on_command_error)

    async def on_command_error(self, ctx, err):
        options = {
            CommandNotFound: self.command_not_found,
            PermissionError: self.permission_denied
        }

        await ctx.send(options.get(type(err), self.report_error)(ctx, err))

    def report_error(self, ctx, err: Exception) -> str:
        stack = '\n'.join(format_exception(type(err), err, err.__traceback__))
        self.log.error(f'encountered {err} exception {stack}')
        return 'encountered an unexpected issue, this interaction has been reported'

    def command_not_found(self, ctx, _) -> str:
        return f'command `{ctx.invoked_with}` not found'

    def permission_denied(self, ctx, _) -> str:
        return f'you do not have sufficient privileges to use the `{ctx.invoked_with}` command`'

    def search_fuzz(self, ctx, items, item: str, msg: str):
        res = fuzzy(items, item)
        if not res:
            return f'no {msg} named {item}'

        names = "  \n".join(res)
        return ctx.embed(f'no {msg} named {item}', f'possible results\n```{names}```')

    def all_cogs(self, ctx) -> Embed:
        fields = { 
            name: body.description for name, body 
                in self.bot.cogs.items() if not body.hidden
        }
        return ctx.embed('all cogs', 'all cogs you have permission to use', fields)

    def cog_help(self, ctx, cog_name: str) -> Embed:
        cog = first(self.bot.cogs.items(), cog_name)
        if not cog or cog.hidden:
            return self.search_fuzz(ctx, self.bot.cogs.keys(), cog_name, 'cog')

        cmds = {
            cmd.name: cmd.brief or cmd.usage for cmd
                in cog.get_commands() if not cmd.hidden
        }

        return ctx.embed(f'all commands in {cog_name}', f'{len(cmds)} total commands', cmds)

    async def cmd_help(self, ctx, name):
        if not name:
            return False

        cmd = self.bot.get_command(name)
        if not cmd or cmd.hidden:
            return False

        details = { 
            'signature': f'```\n{cmd.name} {cmd.signature}```',
            'aliases': ', '.join(cmd.aliases) if cmd.aliases else 'no aliases',
            'usage': (f'```{dedent(cmd.help)}```', False) if cmd.help else 'see signature'
        }

        await ctx.send(embed = ctx.embed(
            cmd.name, cmd.brief,
            details
        ))
        return True

    @command(
        name = 'help',
        brief = 'bot usermanual',
        help = """
        // get general help
        &help

        // get help about a cog
        &help utils

        // get help for a specific command
        &help ping
        """
    )
    async def help(self, ctx: Context, name: str = None):
        # self.cmd_help prints and returns true if it finds a command
        if not await self.cmd_help(ctx, name):
            await ctx.push(self.cog_help(ctx, name.lower()) if name else self.all_cogs(ctx))

    def cog_commands(self, ctx, name: str):
        cog = first(self.bot.cogs.items(), name)

        if not cog:
            return self.search_fuzz(ctx, self.bot.cogs.keys(), name, 'cog')

        cmds = cog.get_commands()
        names = "  \n".join([cmd.name for cmd in cmds])

        return ctx.embed(f'all commands for {name}', f'{len(cmds)} total commands```\n{names}```')

    def all_commands(self, ctx):
        ncogs = 0
        ncmds = 0
        fields = {}

        for it, cog in self.bot.cogs.items():
            if cog.hidden:
                continue

            cmds = cog.get_commands()
            ncogs += 1
            ncmds += len(cmds)
            names = '\n'.join([cmd.name for cmd in cmds])
            fields[it] =  f'```\n{names}```'

        return ctx.embed('all commands', f'{ncogs} cogs containing {ncmds} commands', fields)
        
    @command(
        name = 'commands',
        brief = 'command & module listings',
        help = """
        // list all commands
        &commands

        // list all commands in a specific module
        &help utils
        """
    )
    async def commands(self, ctx: Context, mod: str = None):
        await ctx.send(embed = self.cog_commands(ctx, mod.lower()) if mod else self.all_commands(ctx))

def setup(bot: Claymore):
    bot.help_command = None
    bot.add_cog(Help(bot))
    