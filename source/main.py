import discord
from discord.ext import commands

import configparser
import json

import aiohttp

import os
import sys
#this is the current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

from cogs.store import Store, pyout

import glob

import argparse    
parser = argparse.ArgumentParser(description='another discord bot to steal code from')
parser.add_argument('-r', '--reset', nargs='?', default=False, help='reset all config files')
parser.add_argument('-s', '--silent', nargs='?', default=False, help='supress all errors')
parser.add_argument('-m', '--mac', nargs='?', default=False, help='force mac version')
parser.add_argument('-w', '--windows', nargs='?', default=False, help='force windows version')
parser.add_argument('-l', '--linux', nargs='?', default=False, help='force linux version')
args, leftovers = parser.parse_known_args()

platform = sys.platform.lower()

__version__ = '0.0.1a'

if args.silent is None:
    Store.silent = True

if 'darwin' in platform or args.mac is None:
    Store.current_system = 'mac'
    pyout('Current platform is mac')
elif 'windows' in platform or args.windows is None:
    Store.current_system = 'windows'
    pyout('Current platform is windows')
elif 'linux' in platform or args.linux is None:
    Store.current_system = 'linux'
    pyout('Current platform is a flavor of linux')
else:
    pyout('Undefined system, please start with either -w , -m, -l for windows, mac or linux')

def remove_file(file: str):
    try: os.remove(file)
    except Exception as e: pyout(e)

if args.reset is None:
    remove_file('./cogs/store/config.cfg')

def strtobool(i: str):
    i = i.lower()
    if i in ['yes', 'y', 'true', 't', '1']:
        return True
    elif i in ['no', 'n', 'false', 'f', '0']:
        return False
    raise ValueError('Requires boolean')

def ensure_input(prompt: str, error: str):
    while True:
        ret = input(prompt+'\n').strip()
        if ret =='':
            pyout(error+'\n')
            continue
        return ret

def ensure_bool_input(prompt: str, error: str):
    while True:
        try:
            return strtobool(ensure_input(prompt, error))
        except Exception:
            continue

if not os.path.isfile('./cogs/store/config.cfg'):
    if Store.silent:
        print('You have silent mode enabled, so the setup can not be completed')
        exit(2)
        #exit with code 2 for bad args

    file = open('./cogs/store/config.cfg', 'w')

    print('Seeing as the config file cannot be found')
    print('I need you to input some tokens and keys for me to function properly')

    discord_token = ensure_input('Please input your discord token', 'You need to enter a token')
    discord_prefix = ensure_input('Please enter your bots prefix', 'You need to add a prefix')
    
    discord_activity = input('What would you like my default activity to be? (defaults to help)').strip()

    if discord_activity == '':
        discord_activity = '{}help'.format(discord_prefix)
            
    reddit = ensure_bool_input('Would you like to enable reddit?', 'must be yes or no')
    
    #make everything none by default
    reddit_id = reddit_secret = reddit_username = reddit_password = reddit_message = None

    if reddit:
        reddit_id = ensure_input('Please input your reddit id', 'You must enter an id')
        reddit_secret = ensure_input('Please input your reddit secret', 'You must enter a secret')
        reddit_username = ensure_input('What is your reddit username?', 'you must enter a username')
        reddit_password = ensure_input('What is your reddit password', 'you must enter a password')
        reddit_message = ensure_input('What would you like your reddit bots description to be?', 'you must enter a description')

    wolfram = ensure_bool_input('Would you like to enable this bots wolfram access?', 'must be yes or no')
    
    wolfram_key = None

    if wolfram:
        wolfram_key = ensure_input('Please input your wolfram alpha id', 'you must enter an id')

    #todo
    # google
    # twitter
    # reddit
    # urban dictionary
    # wikipedia
    # wikia fandom wikis
    # random number stuff
    # text fuckery
    # tags
    # quotes
    # warframe
    # blacklist
    # discord email

    # bot owner only
    # block
    # whitelist

    file.write('''[DISCORD]
token = {discord_token}
prefix = {discord_prefix}
activity = {discord_activity}
    
[REDDIT]
enabled = {reddit_enabled}
id = {reddit_id}
secret = {reddit_secret}
username = {reddit_username}
password = {reddit_password}
message = {reddit_message}
    
[WOLFRAM]
enabled = {wolfram_enabled}
key = {wolfram_key}'''.format(
        discord_token=discord_token,
        discord_prefix=discord_prefix,
        discord_activity=discord_activity,
        
        reddit_enabled=reddit,
        reddit_id=reddit_id,
        reddit_secret=reddit_secret,
        reddit_username=reddit_username,
        reddit_password=reddit_password,
        reddit_message=reddit_message,

        wolfram_enabled=wolfram,
        wolfram_key=wolfram_key
    ))
    
    file.close()
    print('Config fully written')
    print('You can edit this at anytime by either reseting the config and running the wizard again')
    print('or you can edit the cofig files directly in cogs/store/config.cfg')

config = configparser.ConfigParser()
config.read('./cogs/store/config.cfg')

def ensure_file(ensure: str, default: str):
    if not os.path.isfile(ensure):
        file = open(ensure, 'w')
        file.write(default)
        file.close()
        return True
    return False

if ensure_file('./cogs/store/bot.log', 'logging file \n'):
    pyout('logfile was generated')

if ensure_file('./cogs/store/direct.log', 'direct messages file \n'):
    pyout('direct messages was generated')

statistic_dict = {
    "messages_processed": 0,
    "commands_used": 0
}

if ensure_file('./cogs/store/statistics.json', json.dumps(statistic_dict, indent=4)):
    pyout('statistics file was generated')

if ensure_file('./cogs/store/symbiosis.json', '[]'):
    pyout('symbiosis file was generated')

if ensure_file('./cogs/store/tags.json', '[]'):
    pyout('tags file was generated')

if ensure_file('./cogs/store/quotes.json', '[]'):
    pyout('quotes file was generated')

if ensure_file('./cogs/store/autoreact.json', '[]'):
    pyout('autoreact file was generated')

if ensure_file('./cogs/store/autorole.json', '[]'):
    pyout('autorole file was generated')

if ensure_file('./cogs/store/disabled.json', '[]'):
    pyout('disabled file was generated')

if ensure_file('./cogs/store/blacklist.json', '[]'):
    pyout('blacklist file was generated')

if ensure_file('./cogs/store/blocked.json', '[]'):
    pyout('blocked file was generated')

if ensure_file('./cogs/store/whitelist.json', '[]'):
    pyout('whitelist file was generated')

bot = commands.Bot(command_prefix=config['DISCORD']['prefix'],
    activity=discord.Game(name=config['DISCORD']['activity']),
    pm_help=None
)

bot.remove_command('help')

@bot.event
async def on_ready():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.warframestat.us/warframes') as resp:
            pyout('Warframe frame data was aquired')
            Store.frames = json.loads(await resp.text())
    pyout('\n+----------------------------------')
    pyout('|my name is: {}#{}'.format(bot.user.name, bot.user.discriminator))
    pyout('|my id is: {}'.format(bot.user.id))
    pyout('+----------------------------------')
    pyout('\nrunning with {} of the discord.py library'.format(discord.__version__))
    pyout('bot version: {}'.format(__version__))
    pyout('bot ready')

try:
    current_stats = json.load(open('./cogs/store/statistics.json'))
except json.decoder.JSONDecodeError:
    ensure_file('./cogs/store/statistics.json', statistic_dict)
    pyout('The statistics file was corrupted so the file has been reset')

async def is_direct(message):
    return isinstance(message.channel, discord.channel.DMChannel) and message.author.id != message.channel.me.id and not message.content.startswith(config['DISCORD']['prefix'])

def save_stats():
    f=open('./cogs/store/statistics.json', 'w')
    f.write(json.dumps(current_stats, indent=4))
    f.close()

@bot.event
async def on_message(message):
    current_stats['messages_processed'] += 1
    await bot.process_commands(message)
    if message.content.startswith(config['DISCORD']['prefix']):
        current_stats['commands_used'] += 1
    save_stats()
    if await is_direct(message):
        pyout(message.author.name + 'says in direct messages ' + message.content)

#@bot.event
#async def on_command_error(ctx, exe):
#    pass

@bot.event
async def on_guild_join(guild):
    pass

@bot.event
async def on_member_leave(member):
    pass

@bot.event
async def on_member_join(member):
    pass

cogs = []

for a in glob.glob('./cogs/*.py'):
    a = a.replace('./cogs/', '')
    a = a.replace('.py', '')
    a = 'cogs.' + a
    if not a in ['cogs.store', 'cogs.__init__']:
        cogs.append(a)

failed_cogs = [

]

if __name__ == '__main__':
    for cog in cogs:
        try: 
            bot.load_extension(cog)
        except Exception as e: 
            pyout(e)
            failed_cogs.append(cog)
    if failed_cogs:
        pyout('These cogs failed')
        pyout(', '.join(failed_cogs))

    try:
        bot.run(config['DISCORD']['token'])
    except discord.errors.LoginFailure:
        print('The token you entered is either incorrect or expired')
        if not Store.silent:
            pyout('The token you entered was either incorrect or expired, but because of silent mode you cannot complete the wizard')
            pyout('Please restart the bot with silent mode enabled to continue')
        else:
            print('The bot is in silent mode, please restart with -r to reset the config and enter the correct token')
        exit(5)
    except Exception as e:
        pyout(e)
        exit(5)
#if it errors exit with 5