from claymore import Wheel
import discord
from discord.ext import commands
import random
from utils import json, can_embed
from random import choice, randint
from pyfiglet import figlet_format

BALL_OPTIONS = [
    'Yes',
    'Outlook good',
    'Almost certainly',
    'Without a doubt',
    'Definetly',

    'No',
    'Not likely',
    'Probably not',
    'Definetly not',
    'Not a chance'
]

class Fun(Wheel):
    @commands.command(name = 'clap')
    async def _clap(self, ctx, *, text: str):
        await ctx.send(' :clap: '.join(text.split(' ')))

    @commands.command(name = 'randomcase')
    async def _randomcase(self, ctx, *, text: str):
        await ctx.send(''.join(random.choice((str.upper, str.lower))(x) for x in text))

    @commands.command(name = 'sawpcase')
    async def _swapcase(self, ctx, *, text: str):
        await ctx.send(text.swapcase())

    @commands.command(name = 'reverse')
    async def _reverse(self, ctx, *, text: str):
        await ctx.send(text[::-1])

    @commands.command(name = 'hash')
    async def _hash(self, ctx, *, text: str):
        await ctx.send(hash(text))

    @commands.command(name = 'expand')
    async def _expand(self, ctx, *, text: str = 'dong'):
        ret = figlet_format(text, font = choice(['big', 'contessa', '5lineoblique', 'alphabet', 'banner', 'doom']))

        if len(ret) < 1900:
            return await ctx.send('Text is too big to send through discord')

        await ctx.send(f'```{ret}```')

    @commands.command(name = 'wolfram')
    async def _wolfram(self, ctx, *, query: str):
        pass

    @commands.command(name = 'reddit')
    async def _reddit(self, ctx, sub: str = 'all', search: str = 'new', index: int = None):
        if index is not None and 0 <= index <= 25:
            return await ctx.send('Index must be between 0 and 25')

        search = search.lower()
        if 'n' in search:
            search = 'new'
        elif 'h' in search:
            search = 'hot'
        elif 't' in search:
            search = 'top'
        else:
            return await ctx.send('Search must be new, hot or top')

        url = f'https://www.reddit.com/r/{sub.lower()}/{search}.json?t=all'

        dat = await json(url)

        if dat.get('error', False):
            return await ctx.send(f'`{sub}` is a private subreddit')

        if not dat['data']['children']:
            return await ctx.send(f'Could not find `{sub}`')

        if index is None:
            post = choice(dat['data']['children'])
        else:
            try:
                post = dat['data']['children'][index]
            except IndexError:
                return await ctx.send(f'There is no post at an index of `{index}`')

        if post['data']['over_18'] and not ctx.channel.is_nsfw():
            return await ctx.send('That post is nsfw, and must be requested in an nsfw channel')

        data = post['data']

        embed = ctx.make_embed(f'Post from {sub}', f'Posted by {data["author"]}')
        embed.add_field(name = 'Link', value = data['url'])
        embed.add_field(name = 'Votes', value = f'{data["ups"]} upvotes & {data["downs"]} downvotes')

        if data['selftext']:
            embed.add_field(name = 'Selftext', value = data['selftext'][:250] + (data['selftext'][250:] and '...'))

        if can_embed(data['url']):
            embed.set_image(url = data['url'])

        await ctx.send(embed = embed)

    @commands.command(name = '8ball')
    async def _8ball(self, ctx, *, thing: str):
        await ctx.send(choice(BALL_OPTIONS))

    @commands.command(name = 'rate')
    async def _rate(self, ctx, *, thing: str):
        await ctx.send(f'I\'d rate {thing} at {randint(0, 10)}/10')

def setup(bot):
    bot.add_cog(Fun(bot))