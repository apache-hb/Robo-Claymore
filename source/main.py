import json
import os
import sys
import traceback
from glob import glob
from shutil import copyfile

import discord
from discord.ext import commands

from cogs.utils.shortcuts import quick_embed

def load_config() -> dict:
    try:
        return json.load(open('cogs/store/config.json'))
    except FileNotFoundError:
        print('The config file was not found, let me run the setup')
        config = {
            'discord': {
                'token': input('Enter bot token'),
                'prefix': input('Enter bot prefix'),
                'activity': input('Enter default bot activity'),
                'owner': input('Enter the owners id')
            },
            'wolfram': {
                'key': input('Enter wolfram-alpha key (optional)')
            },
            'github': {
                'key': input('Enter a github token to enable some commands that send large messages (optional)')
            },
            'count': 0
        }
        json.dump(config, open('cogs/store/config.json', 'w'), indent = 4)
        return config

class ClayBot(commands.Bot):
    def __init__(self, command_prefix: str, activity: discord.Game, owner_id: int, config: dict):
        super(commands.Bot, self).__init__(
            command_prefix = command_prefix, 
            activity = activity, 
            owner_id = owner_id,
            case_insensitive = True
        )
        self.config = config
        self.__version__ = __version__

def make_bot(config: dict) -> ClayBot:
    return ClayBot(
        command_prefix = commands.when_mentioned_or(config['discord']['prefix']),
        activity = discord.Game(name = config['discord']['activity']),
        owner_id = int(config['discord']['owner']),
        config = config
    )

__version__ = '0.4.11'

async def on_ready():
    print('''
name: {0.user.name}#{0.user.discriminator}
id: {0.user.id}
invite: https://discordapp.com/oauth2/authorize?client_id={0.user.id}&scope=bot&permissions=66321471
discord.py version: {1.__version__}
bot version: {2}
bot ready'''.format(bot, discord, __version__))


ignored_errors = [
    commands.errors.CheckFailure,
    commands.errors.CommandNotFound
]

async def after_any_command(ctx):
    logs.write('{0.author.name}#{0.author.id} invoked command {0.invoked_with}\n'.format(ctx))
    logs.flush()

def load_cogs(bot: ClayBot) -> None:
    for cog in glob('cogs/*.py'): #skip __init__ as its not a cog
        if cog in ['cogs/__init__.py']:
            continue

        try:
            bot.load_extension(cog.replace('/', '.')[:-3])#turn cogs/file.py info cogs.file
        except Exception as e:
            print(f'{cog} failed to load becuase: {e}')

def backup_files() -> None:
    os.makedirs('cogs/store/backup/', exist_ok = True)

    #backup all the config files
    for storefile in glob('cogs/store/*.json'):
        copyfile(storefile, f'cogs/store/backup/{os.path.basename(storefile)}')
        print(f'Backed up {storefile}')

if __name__ == '__main__':
    if not os.path.isdir('cogs/store'):
        os.mkdir('cogs/store')

    try:
        logs = open('cogs/store/claymore.log', 'a')
    except FileNotFoundError:
        logs = open('cogs/store/claymore.log', 'w')

    config: dict = load_config()
    bot: ClayBot = make_bot(config)
    load_cogs(bot)
    backup_files()

    bot.add_listener(on_ready)

    #now you may ask why these are in here when add_listener exists
    #this seems to be a bug with discord.py as on_message would fire 3 or 4 times per message
    @bot.event
    async def on_message(context):
        await bot.process_commands(context)

    @bot.event
    async def on_command_error(ctx, exception):
        if any(isinstance(exception, err) for err in ignored_errors):
            return

        if (
            isinstance(exception, commands.errors.MissingRequiredArgument) or
            isinstance(exception, commands.errors.BadArgument)
        ):
            embed = quick_embed(ctx, title = 'Incorrect command usage', description = f'When using command {ctx.command.name}')
            embed.add_field(name = 'The correct usage is', value = ctx.command.signature)
            return await ctx.send(embed = embed)

        elif isinstance(exception, commands.CommandInvokeError):
            if 'Cannot connect to host' in str(exception.original):#there must be a better way of checking error types
                return await ctx.send('My internet connection to that site has been blocked')

        elif isinstance(exception, commands.errors.CommandOnCooldown):
            return await ctx.send(exception)

        elif isinstance(exception.original, TimeoutError):
            return await ctx.send(f'Command {ctx.invoked_with} timed out')

        traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    bot.after_invoke(after_any_command)

    #no point catching exceptions here
    bot.run(config['discord']['token'])
