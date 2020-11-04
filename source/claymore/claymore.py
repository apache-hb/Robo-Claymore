import discord
from discord.ext import commands


import os
import logging
from pymongo import MongoClient

from .utils import ClayContext

class Claymore(commands.Bot):
    def __init__(self, config: dict):
        super().__init__(
            command_prefix = self.get_prefix, 
            activity = discord.Game(name = config['discord']['activity'] or 'help'), 
            owner_id = int(config['discord']['owner'] or 0),
            case_insensitive = True
        )
        self.config = config
        self.db = MongoClient(self.config['mongo']['url'])

    async def get_prefix(self, ctx):
        return self.config['discord']['prefix'] or '&'

    async def on_ready(self):
        logging.info(f'name: {self.user.name}#{self.user.discriminator}')
        logging.info(f'id: {self.user.id}')
        logging.info(f'invite: https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=66321471')
    
    async def get_context(self, msg, *, cls = ClayContext):
        return await super().get_context(msg, cls = ClayContext)
