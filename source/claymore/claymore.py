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

# get the config and create it if it doesnt exist
def get_config():
    path = join('data', 'config.json')
    # if the file exists then just load that in
    if isfile(path) and access(path, R_OK):
        return json.load(open(path, 'r'))
    else:
        # otherwise create it
        data = {
            'discord': {
                'token': input('Input discord bot token'),
                'owner': int(input('Input owner id')),
                'activity': input('Input default activity'),
                'prefix': input('Input default prefix')
            },
            'mongo': {
                'conn': input('Input connection string (dont replace <password>)'),
                'pass': input('Input password')
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

    def __init__(self):
        self.config = get_config()
        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            owner_id = self.config['discord']['owner'],
            activity = discord.Activity(name = self.config['discord']['activity'])
        )
        self.owner = self.config['discord']['owner']
        self.conn = pymongo.MongoClient(self.config['mongo']['conn'].replace('<password>', self.config['mongo']['pass']))
        self.db = self.conn.data

    async def close(self):
        self.conn.close()
        await super().close()

    def run(self):
        super().run(self.config['discord']['token'])

    def get_context(self, msg, *, cls=ClayContext):
        return super().get_context(msg, cls=cls)