import sys
import os

import argparse
import logging
import configparser

from traceback import format_exception
from glob import glob
from claymore import Claymore

parser = argparse.ArgumentParser(description = 'robo-claymore discord bot')
parser.add_argument('--config', help = 'path of config file')
parser.add_argument('--log', help = 'logging output file')

if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(
        filename = args.log or 'claymore.log', 
        level = logging.INFO
    )

    config = configparser.ConfigParser()
    config.read(args.config or 'config.ini')
    bot = Claymore(config)

    cogs = os.path.join(os.path.dirname(__file__), 'cogs')
    globbed = [mod for mod in glob('cogs/*.py') if '__init__' not in mod]

    for cog in globbed:
        try:
            bot.load_extension(cog.replace('.py', '').replace(os.sep, '.'))
        except Exception as e:
            logging.error(f'failed to load {cog}')
            logging.error('\n'.join(format_exception(None, e, e.__traceback__)))

    bot.run(config['discord']['token'])

"""
ignored_errors = [
    commands.errors.CheckFailure,
    commands.errors.CommandNotFound
]

async def after_any_command(ctx):
    try:
        logs.write('{0.author.name}#{0.author.id} invoked command {0.invoked_with}\n'.format(ctx))
        logs.flush()
    except OSError: #during a restart the log file is closed externally s it can error here
        pass

def load_cogs(bot: ClayBot) -> None:
    for cog in glob(os.path.join('cogs', '*.py')): #skip __init__ as its not a cog
        if cog in [os.path.join('cogs', '__init__.py')]:
            continue

        try:
            bot.load_extension(cog.replace(os.sep, '.')[:-3])#turn cogs/file.py info cogs.file
        except Exception as e:
            print(f'{cog} failed to load becuase: {e}')

def backup_files() -> None:
    os.makedirs(os.path.join('cogs', 'store', 'backup'), exist_ok = True)

    #backup all the config files
    for storefile in glob(os.path.join('cogs', 'store', '*.json')):
        copyfile(storefile, os.path.join('cogs', 'store', 'backup', os.path.basename(storefile)))
        print(f'Backed up {storefile}')
"""
"""
if __name__ == '__main__':
    if not os.path.isdir(os.path.join('cogs', 'store')):
        os.mkdir(os.path.join('cogs', 'store'))

    try:
        logs = open(os.path.join('cogs', 'store', 'claymore.log'), 'a')
    except FileNotFoundError:
        logs = open(os.path.join('cogs', 'store', 'claymore.log'), 'w')

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
"""
