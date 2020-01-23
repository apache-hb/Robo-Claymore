from claymore import Wheel
import discord
from discord.ext import commands

class Roles(Wheel):
    def desc(self):
        return 'manage user roles automatically'

def setup(bot):
    bot.add_cog(Roles(bot))
