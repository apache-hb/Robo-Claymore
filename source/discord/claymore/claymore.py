# discord extensions
from discord.ext import commands
import discord

# my own stuff
from .context import Context as ClayContext

# config parsing
import json

# file IO nastyness
from os.path import join, abspath, dirname, isfile
from os import access, R_OK

import pymongo
import logging

# get the config and create it if it doesnt exist
def get_config():
    path = join('..', 'data', 'config.json')
    # if the file exists then just load that in
    if isfile(path) and access(path, R_OK):
        return json.load(open(path, 'r'))
    else:
        # otherwise create it
        conn = input('Input connection string (leave blank if mongodb is hosted locally)')
        data = {
            'discord': {
                'token': input('Input discord bot token'),
                'owner': int(input('Input owner id')),
                'activity': input('Input default activity'),
                'prefix': input('Input default prefix')
            },
            'mongo': {
                'conn': conn if conn else None,
                'name': input('Input database name')
            }
        }

        json.dump(data, open(path, 'w'), indent = 4)
        return data


class Claymore(commands.Bot):
    async def get_prefix(self, msg):
        prefix = self.db.prefix.find_one({ 'id': msg.guild.id })
        default = self.config['discord']['prefix']

        if prefix is not None:
            return (prefix['prefix'], default)

        return default

    async def on_ready(self):
        info = {
            'name': self.user.name,
            'id': self.user.id,
            'dis': self.user.discriminator,
            'avatar': str(self.user.avatar_url)
        }

        json.dump(info, open(join('..', 'data', 'bot_info.json'), 'w'), indent = 4)

        self.log.info(f'Bot logged in as: {self.user.name}#{self.user.discriminator}')
        self.log.info(f'Bot id: {self.user.id}')
        self.log.info(f'Bot invite: https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=66321471')
        self.log.info(f'discord.py version: {discord.__version__}')

    def __init__(self):
        self.log = logging.getLogger('claymore')
        self.log.setLevel(logging.INFO)
        handler = logging.FileHandler(filename = join('..', 'logs', 'bot.log'), encoding = 'utf-8', mode = 'w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(handler)

        self.config = get_config()
        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            owner_id = self.config['discord']['owner'],
            activity = discord.Activity(name = self.config['discord']['activity'])
        )
        self.owner = self.config['discord']['owner']

        if self.config['mongo']['conn'] is None:
            self.conn = pymongo.MongoClient()
        else:
            self.conn = pymongo.MongoClient(self.config['mongo']['conn'])

        self.db = self.conn[self.config['mongo']['name']]
        

    async def close(self):
        self.conn.close()
        await super().close()

    def run(self):
        super().run(self.config['discord']['token'])

    def get_context(self, msg, *, cls=ClayContext):
        return super().get_context(msg, cls=cls)