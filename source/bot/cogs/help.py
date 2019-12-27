import discord
from discord.ext import commands
import claymore
from claymore import Wheel

class Help(Wheel):
    def desc(self):
        return 'help command'

    @commands.command(
        name = 'help',
        brief = 'get help for a commands usage'
    )
    async def _help(self, ctx, *, cmd: str = None):
        if cmd is None:
            # todo print all commands or something
            embed = ctx.make_embed(title = 'Cogs', description = 'All avaiable cogs')

            for cog in self.bot.cogs.values():
                embed.add_field(name = cog.qualified_name, value = cog.desc() if "desc" in dir(cog) else 'No descrption')

            return await ctx.send(embed = embed)

        command = self.bot.get_command(cmd.lower())

        if command is not None:
            prefix = (await self.bot.get_prefix(ctx))
            if isinstance(prefix, tuple):
                prefix = '(' + (' | '.join(prefix)) + ')'

            # we use the full extenson here to prevent some weird errors
            if isinstance(command, discord.ext.commands.Group):
                embed = ctx.make_embed(title = f'Help for command group {cmd}', description = command.brief or 'No description')

                if not command.commands:
                    embed.add_field(name = 'Subcommands', value = 'No subcommands')
                    return await ctx.send(embed = embed)

                for sub in command.commands:
                    embed.add_field(name = sub.name, value = sub.brief)

                return await ctx.send(embed = embed)

            embed = ctx.make_embed(title = f'Help for {cmd}', description = command.brief or 'No description')
            
            if 'usage' in dir(command):
                use = command.usage
            else:
                use = command.signature or ''

            embed.add_field(name = 'Usage', value = f'{prefix}{cmd.lower()} {use}')
            return await ctx.send(embed = embed)

        cog = next((val for key, val in self.bot.cogs.items() if key.lower() == cmd.lower()), None)

        if cog is not None:
            commands = cog.get_commands()
            embed = ctx.make_embed(title = f'All commands for {cmd}', description = f'{len(commands)} total commands')

            for command in commands:
                embed.add_field(name = command.name, value = command.description or 'No description')

            return await ctx.send(embed = embed)

        await ctx.send(f'Nothing found called {cmd}')

def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))