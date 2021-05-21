from claymore import Wheel
import discord
from discord.ext import commands
from utils import can_embed, json
from aiorule34 import rule34get as r34get
from random import choice

class Nsfw(Wheel):
    def desc(self):
        return 'nsfw commands'
        
    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel) or ctx.channel.is_nsfw():
            return True
        await ctx.send('NSFW commands must be used in nsfw channels')
        return False

    @commands.command(
        name = 'rule34',
        brief = 'search rule34.xxx for a post with the desired tags',
        aliases = [ 'r34' ]
    )
    async def _rule34(self, ctx, *, tags: str):
        async with ctx.channel.typing():
            items = []

            async for i in r34get(tags.split()):
                items.append(i)

            post = choice(items)

            embed = ctx.make_embed('A post from rule34.xxx', f'With tags {tags}')
            embed.add_field(name = f'Image source', value = post.url)

            if can_embed(post.url):
                embed.set_image(url = post.url)

            await ctx.send(embed = embed)

    @commands.command(
        name = 'e621',
        brief = 'search e621 for a post'
    )
    async def _e621(self, ctx, *, tags: str = None):
        if tags is None:
            url = 'https://e621.net/post/index.json?limit=25'
        else:
            url = f'https://e621.net/post/index.json?tags={tags}&limit=25'

        async with ctx.channel.typing():
            ret = await json(url)

            if not ret:
                return await ctx.send(f'Nothing with tags `{tags}` found')

            post = choice(ret)

            embed = ctx.make_embed('A post from e621', f'With tags `{tags}`')
            embed.add_field(name = 'Image source', value = post['file_url'])

            if can_embed(post['file_url']):
                embed.set_image(url = post['file_url'])

            await ctx.send(embed = embed)

    @commands.command(
        name = 'gelbooru',
        brief = 'query gelbooru for a post with the desired tags',
        aliases = [ 'gel', 'gb' ]
    )
    async def _gelbooru(self, ctx, *, tags: str):
        async with ctx.channel.typing():
            try:
                ret = await json(f'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags={tags}')
            except ValueError:
                return await ctx.send(f'Nothing with tags `{tags}` found')

            if not ret:
                return await ctx.send(f'Nothing with tags `{tags}` found')

            post = choice(ret)

            embed = ctx.make_embed('A post from gelbooru.com', f'With tags {tags}')
            embed.add_field(name = 'Image source', value = post['file_url'])

            if can_embed(post['file_url']):
                embed.set_image(url = post['file_url'])

            await ctx.send(embed = embed)

    @commands.command(
        name = 'danbooru',
        brief = 'search danbooru for a post',
        aliases = [ 'dan', 'db' ]
    )
    async def _danbooru(self, ctx, *, tags: str = None):
        if tags is None:
            url = 'https://danbooru.donmai.us/posts.json?random=true'
        else:
            url = f'https://danbooru.donmai.us/posts.json?limit=50?tags=\"{tags.split(" ")}\"'

        async with ctx.channel.typing():
            ret = await json(url)

            if not ret:
                return await ctx.send(f'Nothing found with tags `{tags}`')

            post = choice(ret)

            embed = ctx.make_embed('A post from danbooru.com', f'With tags {tags}')
            embed.add_field(name = 'Image source', value = post['large_file_url'])

            if can_embed(post['large_file_url']):
                embed.set_image(url = post['large_file_url'])

            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Nsfw(bot))