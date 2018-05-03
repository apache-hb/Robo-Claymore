from discord.ext import commands
from .store import pyout, style_embed, is_embedable, shorten_url

import aiohttp
import json

config = json.load(open('cogs/store/config.json'))

class Reddit:
    def __init__(self, bot):
        self.bot = bot
        pyout('Cog {} loaded'.format(self.__class__.__name__))

    short = "reddit interface"
    description = "Read posts from anywhere on reddit"

    @commands.command(name="reddit")
    async def reddit(self, ctx, target: str='all', search: str='new', index: int=1):
        if not 0 <= index <= 25:
            return await ctx.send('Index must be within 0 and 25')

        #so i dont have to lower the search each time
        search = search.lower()
        if 'n' in search:
            search = 'new'
        elif 'h' in search:
            search = 'hot'
        elif 't' in search:
            search = 'top'
        else:
            return await ctx.send('Search mode must be new, top or hot')

        to_get = 'https://www.reddit.com/r/{subreddit}/{search_mode}.json?t=all'.format(
            subreddit=target.lower(),
            search_mode=search
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(to_get) as resp:
                j = json.loads(await resp.text())

                if not j['data']['children']:
                    return await ctx.send('No subreddit found')

                post = j['data']['children'][index]

                if post['data']['over_18'] and not ctx.channel.is_nsfw():
                    return await ctx.send('That post is nsfw, and must be requested in an nsfw channel')

                embed=style_embed(ctx, title='Post from {}'.format(target),
                description='Posted by {}'.format(post['data']['author']))

                embed.add_field(name='Link', value=await shorten_url(post['data']['url']))

                embed.add_field(name='Title', value=post['data']['title'])
                embed.add_field(name='Votes', value='{ups} Upvotes & {downs} Downvotes'.format(
                    ups=post['data']['ups'],
                    downs=post['data']['downs']
                ))

                if not post['data']['selftext'] == '':
                    embed.add_field(name='Selftext',
                    value=post['data']['selftext'][:250] + (post['data']['selftext'][250:] and '...'))

                if is_embedable(post['data']['url']):
                    embed.set_image(url=post['data']['url'])

                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Reddit(bot))