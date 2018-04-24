import discord
from discord.ext import commands

class Reddit:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Reddit interface"
    description = "Write posts to the RoboClaymore subreddit, or read posts from anywhere on reddit"
    hidden = False

def setup(bot):
    bot.add_cog(Reddit(bot))