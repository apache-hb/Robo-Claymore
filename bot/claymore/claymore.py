# discord extensions
from discord.ext import commands
import discord

# my own stuff
from .context import Context as ClayContext

# config parsing
import toml

# file IO nastyness
from os.path import abspath, dirname, isfile
from os import access, R_OK

import motor.motor_asyncio as motor
import logging

# get the config and create it if it doesnt exist
def get_config(path: str):
    return toml.load(path)

class Claymore(commands.Bot):
    async def get_prefix(self, msg):
        default = self.config['discord']['prefix']
        if msg.guild is None:
            return default

        prefix = await self.db.prefix.find_one({ 'id': msg.guild.id })

        if prefix is not None:
            return (prefix['prefix'], default)

        return default

    async def on_ready(self):
        await super().change_presence(activity = discord.Game(self.config['discord']['activity']))
        self.log.info(f'logged in as: {self.user.name}#{self.user.discriminator}')
        self.log.info(f'id: {self.user.id}')
        self.log.info(f'invite: https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=66321471')
        self.log.info(f'discord.py version: {discord.__version__}')

    def __init__(self, cfg: str):
        self.log = logging.getLogger('claymore')
        self.log.setLevel(logging.INFO)

        self.log.info(f'loading config from {cfg}')

        self.config = get_config(cfg)
        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            owner_id = int(self.config['discord']['owner']),
            activity = discord.Activity(name = self.config['discord']['activity'])
        )

        self.conn = motor.AsyncIOMotorClient(self.config['mongo']['url'])

        self.db = self.conn[self.config['mongo']['db']]


    async def close(self):
        self.conn.close()
        await super().close()

    def run(self):
        super().run(self.config['discord']['token'])

    def get_context(self, msg, *, cls=ClayContext):
        return super().get_context(msg, cls=cls)