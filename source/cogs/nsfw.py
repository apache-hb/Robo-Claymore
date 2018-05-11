from discord.ext import commands
from .utils import quick_embed, is_embedable, shorten_url
from .store import whitelist

from defusedxml.ElementTree import fromstring
import json
import aiohttp


class Nsfw:
    def __init__(self, bot):
        self.danbooru_thumbnail = 'https://tinyurl.com/ya9ug3la'
        self.bot = bot
        self.loop = 0
        print('Cog {} loaded'.format(self.__class__.__name__))

    async def __local_check(self, ctx):
        if self.bot.is_owner(ctx.author.id):
            return True
        if ctx.author.id in Store.whitelist:  # for some reason doesnt work with an or statement
            return True  # todo debug that

        if ctx.channel.is_nsfw():
            return True
        await ctx.send('Must be used in an nsfw channel')
        return False

    @commands.group(invoke_without_command=True)
    async def tags(self, ctx):
        pass

    @tags.command(name="ban")
    async def _tags_ban(self, ctx, tag: str = None):
        pass

    @tags.command(name="unban")
    async def _tags_unban(self, ctx, tag: str = None):
        pass

    @commands.command(name="danbooru", aliases=['dan', 'db'])
    async def _danbooru(self, ctx, *, tags: str = None):
        if tags is None:
            url = 'https://danbooru.donmai.us/posts.json?random=true'
        else:
            url = 'https://danbooru.donmai.us/posts.json?limit=50?tags=\"{tags}\"'.format(
                tags=tags.split(' '))
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    j = json.loads(await resp.text())

                    if not j:
                        return await ctx.send('Nothing found')

                    # todo there has to be a nicer way of doing this
                    while True:
                        try:
                            post = j[self.loop]
                            self.loop += 1
                            break
                        except IndexError:
                            self.loop = 0

                    embed = quick_embed(
                        ctx,
                        title='A post from danbooru',
                        description='Posted by {}'.format(
                            post['uploader_name']))

                    tags = post['tag_string'].split(' ')

                    embed.set_footer(
                        text='With tags {}'.format(', '.join(tags)),
                        icon_url=self.danbooru_thumbnail)

                    if is_embedable(post['large_file_url']):
                        embed.set_image(url=post['large_file_url'])

                    embed.add_field(
                        name='Image source',
                        value=await shorten_url(post['large_file_url']))

                    await ctx.send(embed=embed)

        except aiohttp.client_exceptions.ClientConnectionError:
            return await ctx.send(
                'Danbooru is currently blocked because of my retarded internet'
            )

    @commands.command(name='rule34', aliases=['r34'])
    async def _rule34(self, ctx, *, tags: str = None):
        if tags is None:
            return await ctx.send(
                'Due to current api limitations, you must request tags')

        url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={tags}'.format(
            tags=tags.replace(' ', '%20'))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    root = fromstring(await resp.text())
                    # todo find a way to get the image url from a json return
                    # to eliminate xml dependancy

                    if root == 0:
                        return await ctx.send(
                            'Nothing with tags {} found'.format(tags))

                    while True:
                        try:
                            post = root[self.loop]
                            self.loop += 1
                            break
                        except IndexError:
                            self.loop = 0

                    info = post.attrib
                    # todo alot of testing
                    tags = info['tags']
                    file_url = info['file_url']

                    embed = quick_embed(ctx, title='Image from gelbooru')
                    embed.add_field(
                        name='Image source', value=await shorten_url(file_url))

                    if is_embedable(url=file_url):
                        embed.set_image(url=file_url)

                    formatted_tags = ''.join(tags)
                    formatted_tags = formatted_tags.split(' ')

                    embed.set_footer(text='With tags {}'.format(
                        ', '.join(formatted_tags[1:-1])))

                    await ctx.send(embed=embed)

        except aiohttp.client_exceptions.ClientConnectionError:
            return await ctx.send(
                'Danbooru is currently blocked because of my retarded internet'
            )

    @commands.command(name='gelbooru', aliases=['gel', 'gb'])
    async def _gelbooru(self, ctx, *, tags: str = None):
        if tags is None:
            return await ctx.send(
                'Due to current api limitations, you must request tags')

        url = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags={tags}'.format(
            tags=tags.replace(' ', '%20'))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        j = json.loads(await resp.text())
                    except ValueError:
                        return await ctx.send(
                            'Nothing with tags {} found'.format(tags))

                    while True:
                        try:
                            post = j[self.loop]
                            self.loop += 1
                            break
                        except IndexError:
                            self.loop = 0

                    embed = quick_embed(
                        ctx,
                        title='A post from gelbooru',
                        description='Posted by {}'.format(post['owner']))

                    tags = post['tags'].split(' ')

                    # todo find gelbooru thumbnail
                    embed.set_footer(
                        text='With tags {}'.format(', '.join(tags)))

                    if is_embedable(post['file_url']):
                        embed.set_image(url=post['file_url'])

                    embed.add_field(
                        name='Image source',
                        value=await shorten_url(post['file_url']))

                    await ctx.send(embed=embed)

        except aiohttp.client_exceptions.ClientConnectionError:
            return await ctx.send(
                'Danbooru is currently blocked because of my retarded internet'
            )


def setup(bot):
    bot.add_cog(Nsfw(bot))
