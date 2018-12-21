import discord
from discord.ext import commands

class Polls:
    def __init__(self, bot):
        self.bot = bot
        print(f'cog {self.__class__.__name__} loaded')

def setup(bot):
    bot.add_cog(Polls(bot))