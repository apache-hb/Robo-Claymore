import discord
from discord.ext import commands
from .store import whitelist, tinyurl, embedable, quick_embed

from defusedxml.ElementTree import fromstring
import json
import aiohttp
import random

class Nsfw:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        print('cog {} loaded'.format(self.__class__.__name__))

    @commands.command(name = "e621")
    async def _esixtwoone(self, ctx, *, tags: str = None):

        if tags is None:
            url = 'https://e621.net/post/index.json?limit=25'

        else:
            url = 'https://e621.net/post/index.json?tags={}&limit=25'.format(tags)

        headers = {
            'User-Agent': 'RoboClaymore (by ApacheActual#6945 on discord)'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers = headers) as resp:

                ret = json.loads(await resp.text())

                if not ret:
                    return await ctx.send('Nothing with tags {} found'.format(tags))

                post = random.choice(ret)

                embed = quick_embed(ctx, title = 'A post from e621')
                embed.add_field(name = 'Image source', value = await tinyurl(post['file_url']))

                if embedable(post['file_url']):
                    embed.set_image(url = post['file_url'])

                await ctx.send(embed = embed)

    @commands.command(name = "rule34", aliases = ['r34'])
    async def _rule34(self, ctx, *, tags: str):
        url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}'.format(tags)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                root = fromstring(await resp.text())

                if not root:
                    return await ctx.send('Nothing with tags {} found'.format(tags))

                post = random.choice(root)

                info = post.attrib

                tags = info['tags']
                file_url = info['file_url']

                embed = quick_embed(ctx, title = 'A post from rule34.xxx')
                embed.add_field(name = 'Image source', value = await tinyurl(file_url))

                if embedable(file_url):
                    embed.set_image(url = file_url)

                await ctx.send(embed = embed)

    @commands.command(name = "gelbooru", aliases = ['gel', 'gb'])
    async def _gelbooru(self, ctx, *, tags: str):
        url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags={}'.format(tags)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    ret = json.loads(await resp.text())
                except ValueError:
                    return await ctx.send('Nothing with tags {} found'.format(tags))

                post = random.choice(ret)

                embed = quick_embed(ctx, title = 'A post from gelbooru.com')
                embed.add_field(name = 'Image source', value = await tinyurl(post['file_url']))

                if embedable(post['file_url']):
                    embed.set_image(url = post['file_url'])

                return await ctx.send(embed = embed)

    @commands.command(name = "danbooru")
    async def _danbooru(self, ctx, *, tags: str = None):
        if tags is None:
            url = 'https://danbooru.donmai.us/posts.json?random=true'

        else:
            url = 'https://danbooru.donmai.us/posts.json?limit=50?tags=\"{}\"'.format(tags.split(' '))

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                ret = json.loads(await resp.text())

                if not ret:
                    return await ctx.send('Nothing found')

                post = random.choice(ret)

                embed = quick_embed(ctx, title = 'An image from danbooru')
                embed.add_field(name = 'Image source', value = await tinyurl(post['large_file_url']))

                if embedable(post['large_file_url']):
                    embed.set_image(url = post['large_file_url'])

                return await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Nsfw(bot))