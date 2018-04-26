import discord
from discord.ext import commands
from .store import Store, pyout

import sys
if Store.current_system == 'mac':
    sys.path.append('/usr/local/lib/python3.6/site-packages')

import praw
import prawcore

import configparser

config = configparser.ConfigParser()
config.read('cogs/store/config.cfg')

class Reddit:
    def __init__(self, bot):
        self.bot = bot
        if config['REDDIT']['enabled'] == 'True':
            self.reddit_client = praw.Reddit(client_id = config['REDDIT']['id'],
                client_secret = config['REDDIT']['secret'],
                password = config['REDDIT']['password'],
                username = config['REDDIT']['username'],
                user_agent = config['REDDIT']['message'])
            pyout('Praw loaded')

        pyout('Cog {} loaded'.format(self.__class__.__name__))

    short = "Reddit interface"
    description = "Write posts to the RoboClaymore subreddit, or read posts from anywhere on reddit"
    hidden = True

    async def __local_check(self, ctx):
        return config['REDDIT']['enabled'] == 'True'

    @commands.group(invoke_without_command=True)
    async def reddit(self, ctx):
        pass

    @reddit.command(name="post")
    async def _post(self, ctx, *, content: str):
        content = content.split('|')
        title = content[0]
        try:
            post = content[1]
        except Exception:
            return await ctx.send('You need to also post a text body')

    @reddit.command(name="get")
    async def _get(self, ctx, sub: str, sorting: str, search: str):
        pass

def setup(bot):
    bot.add_cog(Reddit(bot))