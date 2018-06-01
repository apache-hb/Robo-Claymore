import discord
from discord.ext import commands
import json
from glob import glob
import aiohttp
import traceback
import sys
from cogs.store import whitelist, blacklist, config, quick_embed, logs

bot = commands.Bot(
    command_prefix = config['discord']['prefix'],
    activity = discord.Game(name = config['discord']['activity']),
    owner_id = int(config['discord']['owner']))

#get rid of the help command to allow for a custom one
bot.remove_command('help')

__version__ = '0.0.1.0a'

@bot.event
async def on_ready():
    print('''
name: {name}#{dis}
id: {id}
invite: https://discordapp.com/oauth2/authorize?client_id={id}&scope=bot&permissions=66321471
discord.py version: {discord}
bot version: {bot}
bot ready'''.format(name = bot.user.name, dis = bot.user.discriminator, id = bot.user.id, discord = discord.__version__, bot = __version__))

@bot.event
async def on_message(context):
    await bot.process_commands(context)

@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, discord.ext.commands.errors.MissingRequiredArgument):
        embed = quick_embed(ctx, title = 'Incorrect command usage', description = 'When using command {}'.format(ctx.command.name))
        embed.add_field(name = 'The correct usage is', value = ctx.command.signature)
        return await ctx.send(embed = embed)

    elif isinstance(exception, discord.ext.commands.errors.CheckFailure):
        return

    elif isinstance(exception, discord.ext.commands.errors.CommandNotFound):
        return

    elif isinstance(exception, discord.ext.commands.CommandInvokeError):
        if 'Cannot connect to host' in str(exception.original):
            return await ctx.send('My internet connection to that site has been blocked')

    traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

@bot.check
async def check_commands(ctx):
    #let the bot owner and whitelisted users always override
    if ctx.bot.is_owner(ctx.author) or ctx.author.id in whitelist:
        return True

    if ctx.author.id in blacklist:#make sure to tell blocked people to eat pant
        await ctx.send('Go away')
        return False

    if ctx.command.name.lower() in config['disabled']['commands']:
        await ctx.send('That command has been disabled globally')
        return False

    if ctx.command.name.cog_name.lower() in config['disabled']['cogs']:
        await ctx.send('That cog has been disabled globally')
        return False

    return True

@bot.after_invoke
async def after_any_command(ctx):
    logs.append('{}#{} invoked command {}'.format(
        ctx.author.name,
        ctx.author.id,
        ctx.invoked_with
    ))
    json.dump(logs, open('cogs/store/logs.json', 'w'), indent = 4)

    if ctx.cog.__class__.__name__ == 'Owner':#specifically log if an owner oly command is used
        print('{} tried to use {}'.format(
            ctx.author.name,
            ctx.invoked_with
        ))

if __name__ == '__main__':
    for cog in glob('cogs/*.py'):
        if not cog in ['cogs/__init__.py', 'cogs/store.py']:
            try:
                bot.load_extension(cog.replace('cogs/', 'cogs.').replace('.py', ''))
            except Exception as e:
                print(cog, 'failed to load becuase: ', e)

#no point catching exceptions here
bot.run(config['discord']['token'])