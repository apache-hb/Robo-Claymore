import discord
from discord.ext import commands
from .store import Store, pyout, style_embed, is_embedable, shorten_url


import sys
if Store.current_system == 'mac':
    sys.path.append('/usr/local/lib/python3.6/site-packages')

import praw
import prawcore
from re import search as rs

import json

config = json.load(open('cogs/store/config.json'))

class Reddit:
    def __init__(self, bot):
        self.bot = bot
        if not config['reddit']['id'] is None:
            self.reddit_client = praw.Reddit(
                client_id = config['reddit']['id'],
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
        if not config['reddit']['id'] is None:
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
    async def _get(self, ctx, target: str='all', search: str='top', index: int=1):
        if not 0 <= index <= 100:
            return await ctx.send('Index ``{}`` is out of range, must be within 0 and 100'.format(index))
        try:
            self.reddit_client.subreddits.search_by_name(target, exact=True)
            subreddit = self.reddit_client.subreddit(target)
        except prawcore.exceptions.NotFound:
            return await ctx.send('No subreddit called ``{}`` found'.format(target))
        except prawcore.exceptions.Redirect:
            return await ctx.send('That subreddit is private')

        if search.find('n'):
            posts = subreddit.new(limit=index+2)
        elif search.find('t'):
            posts = subreddit.top(limit=index+2)
        elif search.find('h'):
            posts = subreddit.hot(limit=index+2)
        else:
            await ctx.send('The search mode {} is not valid'.format(search))

        try: 
            posts
        except prawcore.exceptions.Forbidden:
            return await ctx.send('That subreddit is private')

        a=-1
        for post in posts:
            if not post.stickied:
                a+=1
                if a == index:
                    if not ctx.bot.is_owner(ctx.author):
                        if post.over_18 and not ctx.channel.is_nsfw():
                            return await ctx.send('This post has been marked as nsfw, I can\'t post it here')

                    embed=style_embed(ctx, title='Reddit post from {}'.format(subreddit.display_name),
                    description='Posted by {}'.format(post.author.name))

                    if is_embedable(url=post.url):
                        embed.set_image(url=post.url)
                    elif rs('[a-zA-Z]', post.selftext):
                        text = post.selftext[:250] + (post.selftext[250:] and '...')
                        embed.add_field(name='Post text', value=text, inline=False)
                    embed.add_field(name='Post url', value=await shorten_url(post.url))
                    embed.add_field(name='Post title', value=post.title)
                    return await ctx.send(embed=embed)
        return await ctx.send('Nothing found')

def setup(bot):
    bot.add_cog(Reddit(bot))