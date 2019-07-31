import discord
from discord.ext import commands

class Wheel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db

