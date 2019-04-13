import json
import random

from defusedxml.ElementTree import fromstring
from discord.ext import commands

from .utils import skkcomplex_request
from .utils.networking import json_request, tinyurl, url_request
from .utils.shortcuts import embedable, quick_embed
from .utils.converters import image_to_bytes

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'cog {self.__class__.__name__} loaded')

    @commands.command(
        name = "e621",
        description = "search for an image from e621",
        brief = "degenerate"
    )
    async def _e_six_two_one(self, ctx, *, tags: str = None):

        if tags is None:
            url = 'https://e621.net/post/index.json?limit=25'
        else:
            url = f'https://e621.net/post/index.json?tags={tags}&limit=25'

        headers = {
            'User-Agent': 'RoboClaymore (by ApacheActual#6945 on discord)'
        }

        async with ctx.channel.typing():
            ret = json.loads(await url_request(url = url, headers = headers))

            if not ret:
                return await ctx.send(f'Nothing with tags ``{tags}`` found')

            post = random.choice(ret)

            embed = quick_embed(ctx, title = 'A post from e621')
            embed.add_field(name = 'Image source', value = await tinyurl(post['file_url']))

            if embedable(post['file_url']):
                embed.set_image(url = post['file_url'])

            await ctx.send(embed = embed)

    rule34_api = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}'

    @commands.command(
        name = "rule34",
        aliases = ['r34'],
        description = "search for an image from rule34.xxx",
        brief = "pip install aiorule34"
    )
    async def _rule34(self, ctx, *, tags: str):
        async with ctx.channel.typing():
            root = fromstring(await url_request(url = self.rule34_api.format(tags)))

            if not root:
                return await ctx.send(f'Nothing with tags ``{tags}`` found')

            info = random.choice(root).attrib

            tags = info['tags']
            file_url = info['file_url']

            embed = quick_embed(ctx, title = 'A post from rule34.xxx')
            embed.add_field(name = 'Image source', value = await tinyurl(file_url))

            if embedable(file_url):
                embed.set_image(url = file_url)

            await ctx.send(embed = embed)

    gelbooru_api = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags={}'

    @commands.command(
        name = "gelbooru",
        aliases = ['gel', 'gb'],
        description = "search for an image in gelbooru",
        brief = "the only nice booru api out there"
    )
    async def _gelbooru(self, ctx, *, tags: str):
        async with ctx.channel.typing():
            try:
                ret = await json_request(self.gelbooru_api.format(tags))
            except ValueError:
                return await ctx.send(f'Nothing with tags ``{tags}`` found')

            post = random.choice(ret)

            embed = quick_embed(ctx, title = 'A post from gelbooru.com')
            embed.add_field(name = 'Image source', value = await tinyurl(post['file_url']))

            if embedable(post['file_url']):
                embed.set_image(url = post['file_url'])

            return await ctx.send(embed = embed)

    @commands.command(
        name = "danbooru",
        aliases = ['dan', 'db'],
        description = "search for an image in danbooru",
        brief = "the closest to a SFW booru"
    )
    async def _danbooru(self, ctx, *, tags: str = None):
        if tags is None:
            url = 'https://danbooru.donmai.us/posts.json?random=true'
        else:
            url = f'https://danbooru.donmai.us/posts.json?limit=50?tags=\"{tags.split(" ")}\"'
        
        async with ctx.channel.typing():
            ret = await json_request(url)

            if not ret:
                return await ctx.send('Nothing found')

            post = random.choice(ret)

            embed = quick_embed(ctx, title = 'An image from danbooru')
            embed.add_field(name = 'Image source', value = await tinyurl(post['large_file_url']))

            if embedable(post['large_file_url']):
                embed.set_image(url = post['large_file_url'])

            return await ctx.send(embed = embed)

    @commands.command(
        name = "gif",
        description = "a porn gif",
        brief = "at least its normal"
    )
    async def _gif(self, ctx):
        r = await json_request('https://nekobot.xyz/api/image?type=pgif')
        embed = quick_embed(ctx, 'its gif not jif')
        embed.set_image(url = r['message'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "4k",
        description = "get a 4k prawn image",
        brief = "high quality"
    )
    async def _4k(self, ctx):
        r = await json_request('https://nekobot.xyz/api/image?type=4k')
        embed = quick_embed(ctx, 'imagine how much that camera cost')
        embed.set_image(url = r['message'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "pussy",
        description = "do i have to explain this?",
        brief = "really tho"
    )
    async def _pussy(self, ctx):
        r = await json_request('https://nekobot.xyz/api/image?type=pussy')
        embed = quick_embed(ctx, 'not catgirls')
        embed.set_image(url = r['message'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "hentai",
        description = "get hentai",
        brief = "its called art"
    )
    async def _hentai(self, ctx):
        r = await json_request('https://nekobot.xyz/api/image?type=hentai')
        embed = quick_embed(ctx, 'Its called hetai, and its art')
        embed.set_image(url = r['message'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "neko",
        description = "get a questionable neko image",
        brief = "Y tho?"
    )
    async def _neko(self, ctx):
        r = await json_request('https://nekobot.xyz/api/image?type=lewdneko')
        embed = quick_embed(ctx, 'Elon musk should make them a reality')
        embed.set_image(url = r['message'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "safeneko",
        description = "even if it is sfw its staying in nsfw",
        brief = "miss me with that anime shit"
    )
    async def _safeneko(self, ctx):
        r = await json_request('https://nekos.life/api/v2/img/neko')
        embed = quick_embed(ctx, 'jesus is still dissapointed')
        embed.set_image(url = r['url'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "anal",
        description = "i dont want to have to write this",
        brief = "why am i even doing this"
    )
    async def _anal(self, ctx):
        r = await json_request('https://nekobot.xyz/api/image?type=hentai_anal')
        embed = quick_embed(ctx, 'wake me up inside')
        embed.set_image(url = r['message'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "holo",
        description = "i dont even watch anime",
        brief = "what even is this?"
    )
    async def _holo(self, ctx):
        r = await json_request('https://nekos.life/api/v2/img/hololewd')
        embed = quick_embed(ctx, 'what even')
        embed.set_image(url = r['url'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "gasm",
        description = "at least this one is self explanitory",
        brief = "im pretty sure theres a picture of jontron in there as well"
    )
    async def _gasm(self, ctx):
        r = await json_request('https://nekos.life/api/v2/img/gasm')
        embed = quick_embed(ctx, 'yeet')
        embed.set_image(url = r['url'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "kitsune",
        description = "apparently its a foxgirl",
        brief = "but catgirls already exist"
    )
    async def _kitsune(self, ctx):
        r = await json_request('https://nekobot.xyz/api/image?type=lewdkitsune')
        embed = quick_embed(ctx, 'can i get uHHHHHHHH')
        embed.set_image(url = r['message'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "sankakucomplex",
        aliases = ['skk', 'complex', 'sankaku'],
        description = "get a post from chan.sankakucomplex.com",
        brief = "api machine broke"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _skk(self, ctx, *, tags: str):
        async with ctx.channel.typing():
            msg = await ctx.send('Requesting from sankakucomplex.com, this will take a while')

            try:
                array = await skkcomplex_request(tags)
            except TypeError:
                return await msg.edit(content = 'Im being ratelimited by sankaku, if you know how the fuck to work the api, do tell me')

            try:
                choice = 'https:' + random.choice(array)
                await msg.edit(content = 'Found an image')
                await ctx.send(choice)
            except IndexError:
                return await msg.edit(content = f'Nothing found with the tags ``{tags}``')

def setup(bot):
    bot.add_cog(Nsfw(bot))
