import discord
from discord.ext import commands
from .store import Store, pyout

import sys
if Store.current_system == 'mac':
    sys.path.append('/usr/local/lib/python3.6/site-packages')

import praw
import prawcore

import json

config = json.load(open('cogs/store/config.json'))

class Reddit:
    def __init__(self, bot):
        self.bot = bot
        if not config['reddit']['id'] is None:
            self.reddit_client = praw.reddit(client_id = config['reddit']['id'],
                client_secret = config['reddit']['secret'],
                password = config['reddit']['password'],
                username = config['reddit']['username'],
                user_agent = config['reddit']['message'])
            pyout('Praw loaded')

        pyout('Cog {} loaded'.format(self.__class__.__name__))

    short = "reddit interface"
    description = "Write posts to the RoboClaymore subreddit, or read posts from anywhere on reddit"
    hidden = True

    async def __local_check(self, ctx):
        if config['reddit']['enabled'] == 'True':
            return True
        await ctx.send('Reddit has been disabled')
        return False

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