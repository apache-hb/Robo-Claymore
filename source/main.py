from glob import glob
import json
import os
import sys
import traceback

import aiohttp
import discord
from discord.ext import commands

from cogs.store import (
    config, stats, frames,
    whitelist, blacklist)

__version__ = '0.0.1.4a'

bot = commands.Bot(
    command_prefix=config['discord']['prefix'],
    activity=discord.Game(name=config['discord']['activity'])
)

bot.remove_command('help')

@bot.event
async def on_ready():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.warframestat.us/warframes') as resp:
            print('warframe data aquired')
            frames = json.loads(await resp.text())
    print('''
--------------------------------------
my name is: {name}#{discrim}
my id is: {id}
invite me with: https://discordapp.com/oauth2/authorize?client_id={id}&scope=bot&permissions=66321471
--------------------------------------
running with version {discord} of discord.py
bot version: {bot}
bot ready
    '''.format(
        name=bot.user.name,
        discrim=bot.user.discriminator,
        id=bot.user.id,
        discord=discord.__version__,
        bot=__version__
    ))

@bot.event
async def on_message(message):
    stats['total_messages']+=1
    await bot.process_commands(message)

    #stop autoreact from trying to react in direct messages
    if message.guild is None:
        return

@bot.after_invoke
async def after_any_command(ctx):
    stats['total_commands']+=1

@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, discord.ext.commands.errors.CheckFailure):
        return await ctx.send('You do not have the required permissions to do that')
    elif isinstance(exception, discord.ext.commands.errors.MissingRequiredArgument):
        return await ctx.send('You have missing arguments')
    elif isinstance(exception, discord.ext.commands.CommandNotFound):
        return

    traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

cogs = []

for a in glob('cogs/*.py'):
    cogs.append(a.replace('.py', '').replace('cogs/', 'cogs.'))

cogs.remove('cogs.__init__')
cogs.remove('cogs.store')
cogs.remove('cogs.utils')

failed_cogs = []

if __name__ == '__main__':
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(e)
            failed_cogs.append(cog)
    if failed_cogs:
        print('these cogs failed\n','\n'.join(failed_cogs))
    else:
        print('all cogs loaded successfully')

#no point putting this in a try catch really
bot.run(config['discord']['token'])