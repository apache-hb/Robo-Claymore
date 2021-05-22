import discord
from discord.ext import commands

class Wheel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db
        # this print magically gets the name of the superclass
        self.bot.log.info(f'loaded cog {self.__class__.__name__}')
