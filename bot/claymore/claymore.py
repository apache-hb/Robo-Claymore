import discord
from discord.ext import commands

import os
import logging
from discord.flags import Intents
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient

from .utils import Context

def intents(**kwargs):
    out = Intents.default()
    for k, v in kwargs.items():
        setattr(out, k, v)

    return out

class Claymore(commands.Bot):
    def __init__(self, config: dict):
        super().__init__(
            command_prefix = self.get_prefix, 
            activity = discord.Game(name = config['discord']['activity'] or 'help'), 
            owner_id = int(config['discord']['owner'] or 0),
            case_insensitive = True,
            intents = intents(members = True)
        )
        self.config = config
        # create the mongo client
        dbclient = MotorClient(self.config['mongo']['url'])
        # get our database from the client
        self.db = dbclient[config['mongo']['db']]

    async def get_prefix(self, ctx):
        default = self.config['discord'].get('prefix', '&')

        if not ctx.guild:
            return default

        prefix = (await self.db.config.find_one({ 'id': ctx.guild.id }) or {}).get('prefix', None)

        return (prefix, default) if prefix else default

    async def on_ready(self):
        logging.info(f'name: {self.user.name}#{self.user.discriminator}')
        logging.info(f'id: {self.user.id}')
        logging.info(f'invite: https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=66321471')
    
    async def get_context(self, msg, *, cls = Context):
        return await super().get_context(msg, cls = cls)
