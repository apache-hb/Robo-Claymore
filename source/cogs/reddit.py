import discord
from discord.ext import commands

class Reddit:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Reddit interface"
    description = "Write posts to the RoboClaymore subreddit, or read posts from anywhere on reddit"
    hidden = False

    @commands.group(invoke_without_command=True)
    async def reddit(self, ctx):
        pass

    @reddit.command(name="post")
    async def _post(self, ctx, *, content: str):
        content = content.split('|')
        title = content[0]
        post = content[1]

    @reddit.command(name="get")
    async def _get(self, ctx, sub: str, sorting: str, search: str):
        pass

def setup(bot):
    bot.add_cog(Reddit(bot))