from claymore import Wheel
import discord
from discord.ext import commands

class Fun(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

def setup(bot):
    bot.add_cog(Fun(bot))