import json
import platform
import random
from datetime import datetime
from xml.dom.minidom import parseString

import aiohttp
import discord
from bs4 import BeautifulSoup as bs
from defusedxml.ElementTree import fromstring
from discord.ext import commands
from pyfiglet import figlet_format
from itertools import chain
from urllib.parse import urlencode
import time
from inspect import getsource

from .store import (embedable, emoji_dict, hastebin, hastebin_error,
                    quick_embed, tinyurl, whitelist, config, inverted_dict,
                    ServerNotFound, quotes, tags)

# wikia fandom wikis
WIKIA_API_URL = 'http://{lang}{sub_wikia}.wikia.com/api/v1/{action}'
WIKIA_STANDARD_URL = 'http://{lang}{sub_wikia}.wikia.com/wiki/{page}'
WIKIPEDIA_API_URL = 'http://en.wikipedia.org/w/api.php'

USER_AGENT = '{type} (https://github.com/Apache-HB/Robo-Claymore)'

class Wolfram:
    def __init__(self, key):
        self.key = key
        print('Wolfram loaded')

    async def query(self, question, params=(), **kwargs):
        data = dict(input=question, appid=self.key)
        data = chain(params, data.items(), kwargs.items())
        query = urlencode(tuple(data))
        url = 'https://api.wolframalpha.com/v2/query?' + query
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return fromstring(await resp.text())


class Zalgo:
    def __init__(self, txt: str, intensity: int):
        self.txt = txt
        self.intensity = intensity

    def __str__(self):
        return self.zalgo(text = self.txt, intensity = self.intensity).decode('utf-8')

    def zalgo(self, text, intensity=50):
        zalgo_threshold = intensity
        zalgo_chars = [chr(i) for i in range(0x0300, 0x036F + 1)]
        zalgo_chars.extend([u'\u0488', u'\u0489'])
        source = text.upper()
        if not self._is_narrow_build:
            source = self._insert_randoms(source)
        zalgoized = []
        for letter in source:
            zalgoized.append(letter)
            zalgo_num = random.randint(0, zalgo_threshold) + 1
            for _ in range(zalgo_num):
                zalgoized.append(random.choice(zalgo_chars))
        response = random.choice(zalgo_chars).join(zalgoized)
        return response.encode('utf8', 'ignore')

    @classmethod
    def _insert_randoms(self, text):
        random_extras = [chr(i) for i in range(0x1D023, 0x1D045 + 1)]
        newtext = []
        for char in text:
            newtext.append(char)
            if random.randint(1, 5) == 1:
                newtext.append(random.choice(random_extras))
        return u''.join(newtext)

    @classmethod
    def _is_narrow_build(self):
        try:
            chr(0x10000)
        except ValueError:
            return True
        return False


class Utility:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        self.wolfram = Wolfram(config['wolfram']['key'])
        print('cog {} loaded'.format(self.__class__.__name__))

    @commands.command(name = "zalgo")
    async def _zalgo(self, ctx, *, text: str = 'zalgo 50'):
        text = text.split(' ')
        try:
            intensity = int(text[-1])
        except Exception:
            intensity = 50
            text = ' '.join(text)
        else:
            text = ' '.join(text[:-1])

        if not 1 <= intensity <= 1000:
            return await ctx.send('Intensity must be between 1 and 1000')

        ret = Zalgo(txt = text, intensity = intensity)

        try:
            await ctx.send(ret)
        except Exception:
            await ctx.send(embed = await hastebin_error(ctx, content = ret))

    @commands.command(name = "flip")
    async def _flip(self, ctx, *, text: str):
        ret = ''
        for char in text:
            try: ret += inverted_dict[char.lower()]
            except KeyError: pass

        return await ctx.send(ret)

    @commands.command(name = "staggercase")
    async def _staggercase(self, ctx, *, text: str):
        ret = ''
        upper = True
        for char in text:
            ret += char.upper() if upper else char.lower()
            upper = not upper

        await ctx.send(ret)

    @commands.command(name = "tinyurl")
    async def _tinyurl(self, ctx, *, url: str):
        await ctx.send(await tinyurl(url))

    @commands.command(name = "hastebin")
    async def _hastebin(self, ctx, *, content: str):
        await ctx.send(await hastebin(content))

    @commands.command(name = "hash")
    async def _hash(self, ctx, *, text: str):
        await ctx.send(hash(text))

    @commands.command(name = "reverse")
    async def _reverse(self, ctx, *, text: str):
        await ctx.send(text[::-1])

    @commands.command(name = "invert")
    async def _invert(self, ctx, *, text: str):
        await ctx.send(text.swapcase())

    @commands.command(name = "randomcase")
    async def _randomcase(self, ctx, *, text: str):
        await ctx.send(''.join(random.choice((str.upper, str.lower))(x) for x in text))

    @commands.command(name = "expand")
    async def _expand(self, ctx, *, text: str = 'dong'):
        ret = figlet_format(text, font = random.choice(['big', 'starwars', 'block', 'bubble', 'cards', 'catwalk']))

        if not len(ret) <= 1800:
            return await ctx.send(embed = hastebin_error(ctx, ret))

        await ctx.send('```' + ret + '```')

    @commands.command(name = "emoji")
    async def _emoji(self, ctx, *, text: str = 'Bottom text'):

        ret = ''
        for a in text:
            try:
                ret += emoji_dict[a][0]
            except KeyError:
                ret += emoji_dict[' '][0]

        if not len(ret) <= 1800:
            return await ctx.send(embed = await hastebin_error(ctx, ret))

        await ctx.send(ret)

    @commands.command(name = "binary")
    async def _binary(self, ctx, *, text: str):

        ret = ' '.join(format(ord(x), 'b') for x in text)

        if not len(ret) <= 1800:
            return await ctx.send(embed = await hastebin_error(ctx, ret))

        await ctx.send(ret)

    @commands.command(name = "ascii")
    async def _ascii(self, ctx, *, text: str):

        ret = ''.join(str([ord(c) for c in text]))

        if not len(ret) <= 1800:
            return await ctx.send(embed = await hastebin_error(ctx, ret))

        await ctx.send(ret)

    @commands.command(name = "square")
    async def _square(self, ctx, *, text: str):

        ret = text + '\n'
        for letter in text[1:]:
            ret += letter + '\n'

        if not len(ret) <= 1800:
            return await ctx.send(embed = await hastebin_error(ctx, ret))

        await ctx.send(ret)

    @commands.command(name = "source")
    async def _source(self, ctx, *, name: str = None):

        if name is None:
            return await ctx.send('https://github.com/Apache-HB/Robo-Claymore/tree/Rewrite')

        func = ctx.bot.get_command(name)

        if func is None:
            return await ctx.send('No command called ``{}`` found'.format(name))

        ret = getsource(func.callback)

        if not len(ret) <= 1800:
            return await ctx.send(embed = await hastebin_error(ctx, ret))

        await ctx.send('```py\n' + ret.replace('`', '\`') + '```')

    @commands.command(name = "urban")
    async def _urban(self, ctx, *, search: str = None):

        url = 'http://api.urbandictionary.com/v0/random'

        if not search is None:
            url = 'http://api.urbandictionary.com/v0/define?term=' + search

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                ret = json.loads(await resp.text())

                if not ret['list']:
                    return await ctx.send('Nothing about {} found'.format(search))

                post = random.choice(ret['list'])

                embed = quick_embed(ctx, title = 'Definition of {}'.format(post['word']),
                description = 'Written by {}'.format(post['author']))
                embed.add_field(name = 'Description', value = post['definition'])
                embed.add_field(name = 'Example', value = post['example'])
                embed.add_field(name = 'Permalink', value = post['permalink'])
                embed.set_footer(text = 'Votes: {}/{}'.format(post['thumbs_up'], post['thumbs_down']))

                await ctx.send(embed = embed)

    @commands.command(name = "userinfo")
    async def _userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = quick_embed(ctx,
        title = 'Information about {}#{}'.format(user.name, user.discriminator),
        description = 'User ID: {}'.format(user.id))

        embed.set_thumbnail(url = user.avatar_url)

        now = datetime.now()

        if not ctx.guild is None:
            diffrence = now - user.joined_at
            embed.add_field(name = 'Time spent in {}'.format(ctx.guild.name),
            value = 'First joined at {}, thats over {} days ago'.format(
                user.joined_at.date(),
                diffrence.days
            ), inline = False)

        diffrence = now - user.created_at
        embed.add_field(name = 'Time spent on discord',
        value = 'First joined at {}, thats over {} days ago'.format(
            user.created_at.date(),
            diffrence.days
        ), inline = False)

        if not ctx.guild is None:
            roles = []
            for role in user.roles:
                roles.append(role.name)
            embed.add_field(name = 'Roles', value = ', '.join(roles))
        embed.add_field(name = 'Is the user a bot', value = user.bot)
        await ctx.send(embed = embed)

    @commands.command(name = "selfinfo")
    async def _selfinfo(self, ctx):
        await ctx.invoke(self.bot.get_command('userinfo'))

    @commands.command(name = "serverinfo")
    @commands.guild_only()
    async def _serverinfo(self, ctx):
        embed = quick_embed(ctx, title = 'Server information about {}'.format(ctx.guild.name), description = 'ID: {}'.format(ctx.guild.id))
        now = datetime.now()
        diffrence = now - ctx.guild.created_at
        embed.add_field(name = 'Created at',
        value = '{}, thats over {} days ago'.format(
            ctx.guild.created_at.date(), diffrence.days
        ),inline = False)
        embed.add_field(name = 'User Count', value = len(ctx.guild.members))
        embed.add_field(name = 'Owner', value = ctx.guild.owner.name)
        embed.add_field(name = 'Text channels', value = len(ctx.guild.text_channels))
        embed.add_field(name = 'Voice channels', value = len(ctx.guild.voice_channels))
        embed.set_thumbnail(url = ctx.guild.icon_url)
        await ctx.send(embed = embed)

    @commands.command(name = "botinfo")
    async def _botinfo(self, ctx):
        embed = quick_embed(ctx, title='Info about me, {}'.format(self.bot.user.name))
        embed.add_field(name = 'Working directory', value = dir_path)
        embed.set_thumbnail(url = self.bot.user.avatar_url)
        embed.add_field(name = 'discord.py version', value = discord.__version__)
        embed.add_field(name = 'bot name and id',
        value="Name: {name}, ID: {id}".format(id = self.bot.user.id, name = self.bot.user.name))
        embed.add_field(name = 'Architecture', value = platform.machine())
        embed.add_field(name = 'Version', value = platform.version())
        embed.add_field(name = 'Platform', value = platform.platform())
        embed.add_field(name = 'Processor', value = platform.processor())
        await ctx.send(embed = embed)

    @commands.command(name = "wolfram")
    async def _wolfram(self, ctx, *, question: str):
        if config['wolfram']['key'] == '':
            return await ctx.send('Wolfram has not been setup on this bot')

        embed = quick_embed(ctx, title = 'All possible awnsers from wolfram')
        root = await self.wolfram.query(question)

        for child in root:
            for subobject in child:
                for subsubobject in subobject:
                    if subsubobject.tag == 'plaintext':
                        embed.add_field(name='Possible awnser', value=subsubobject.text)
                        return await ctx.send(embed=embed)


    @commands.command(name = "reddit")
    async def _reddit(self, ctx, target: str = 'all', search: str = 'new', index: int = 1):
        if not 0 <= index <= 25:
            return await ctx.send('Index must be between 0 and 25')

        # so i dont have to lower the search each time
        search = search.lower()
        if 'n' in search:
            search = 'new'
        elif 'h' in search:
            search = 'hot'
        elif 't' in search:
            search = 'top'
        else:
            return await ctx.send('Search mode must be new, top or hot')

        to_get = 'https://www.reddit.com/r/{}/{}.json?t=all'.format(target.lower(), search)

        async with aiohttp.ClientSession() as session:
            async with session.get(to_get) as resp:
                j = json.loads(await resp.text())

                if not j['data']['children']:
                    return await ctx.send('No subreddit found')

                try: post = j['data']['children'][index]
                except IndexError: return await ctx.send('There is no post with that index')

                if not ctx.bot.is_owner(ctx.author) or ctx.author.id in whitelist:
                    if post['data']['over_18'] and not ctx.channel.is_nsfw():
                        return await ctx.send('That post is nsfw, and must be requested in an nsfw channel')

                embed = quick_embed(ctx, title = 'Post from {}'.format(target),
                    description = 'Posted by {}'.format(post['data']['author']))

                embed.add_field(name = 'Link', value = await tinyurl(post['data']['url']))

                embed.add_field(name = 'Title', value = post['data']['title'])
                embed.add_field(name = 'Votes', value = '{} Upvotes & {} Downvotes'.format(
                        post['data']['ups'], post['data']['downs']))

                if not post['data']['selftext'] == '':
                    embed.add_field(name = 'Selftext',
                    value = post['data']['selftext'][:250] + (post['data']['selftext'][250:] and '...'))

                if embedable(post['data']['url']):
                    embed.set_image(url = post['data']['url'])

                return await ctx.send(embed = embed)

    @commands.group(invoke_without_command = True)
    async def prettyprint(self, ctx):
        embed = quick_embed(ctx, title = 'All the things I can prettyprint', description = 'Not that xml will ever be pretty anyway')
        b = []
        for a in self.prettyprint.walk_commands():
            if a.name not in b:
                embed.add_field(name = a.name, value = a.brief)
            b.append(a.name)
        await ctx.send(embed = embed)

    @prettyprint.command(name = "xml")
    async def _prettyprint_xml(self, ctx, *, text: str):
        try:
            ret = parseString(text)
        except Exception:
            return await ctx.send('Cannot prettyprint malformed xml')

        await ctx.send('```xml\n' + ret.toprettyxml() + '```')

    @prettyprint.command(name = "json")
    async def _prettyprint_json(self, ctx, *, text: str):
        try:
            ret = json.loads(text)
        except json.JSONDecodeError:
            return await ctx.send('Cannot prettyprint malformed json')

        await ctx.send('```json\n' + json.dumps(ret, indent = 4).replace('`', '\`') + '```')

    @prettyprint.command(name = "html")
    async def _prettyprint_html(self, ctx, *, text: str):
        try:
            ret = bs(text, 'html.parser').prettify()
        except Exception:
            return await ctx.send('Cannot prettyprint malformed html')

        await ctx.send('```html\n' + ret.replace('`', '\`') + '```')


    @commands.group(invoke_without_command = True)
    @commands.guild_only()
    async def tag(self, ctx, name: str = None):
        for server in tags:
            if server['id'] == ctx.guild.id:

                if not server['contents']:
                    return await ctx.send('this server has no saved tags')

                if name is None:
                    ret = random.choice(server['contents'])
                    return await ctx.send(ret['content'])

                for item in server['contents']:
                    if item['tag'] == name:
                        return await ctx.send(item['content'])

        tags.append({
            'id': ctx.guild.id,
            'contents': [

            ]
        })
        json.dump(tags, open('cogs/store/tags.json', 'w'), indent = 4)
        await ctx.invoke(self.bot.get_command("tag"))

    @tag.command(name = "add")
    async def _tag_add(self, ctx, name: str, *, content: str):
        ret = {
            'tag': name.lower(),
            'content': content
        }
        for server in tags:
            if server['id'] == ctx.guild.id:

                if any(item['tag'] == name.lower() for item in server['contents']):
                    return await ctx.send('That tag already exists')

                server['contents'].append(ret)
                json.dump(tags, open('cogs/store/tags.json', 'w'), indent = 4)
                return await ctx.send('added tag {}'.format(name))


    @tag.command(name = "remove")
    async def _tag_remove(self, ctx, name: str):
        for server in tags:
            if server['id'] == ctx.guild.id:
                for item in server['contents'][:]:
                    if item['tag'] == name.lower():
                        server['contents'].remove(item)
                        json.dump(tags, open('cogs/store/tags.json', 'w'), indent = 4)
                        return await ctx.send('deleted tag {}'.format(name))
                return await ctx.send('not tag called {} found'.format(name))


    @tag.command(name = "list")
    async def _tag_list(self, ctx):
        for server in tags:
            if server['id'] == ctx.guild.id:

                if not server['contents']:
                    return await ctx.send('this server has no tags')

                ret = ''
                for pair in server['contents']:
                    ret += pair['tag'] + '\n'

                if len(ret) > 2000:
                    [ret[i:i+1500] for i in range(0, len(ret), 1500)]

                    for part in ret:
                        await ctx.author.send('```\n' + part + '```')

                else:
                    return await ctx.author.send('```\n' + ret + '```')

    @commands.group(invoke_without_command = True)
    @commands.guild_only()
    async def quote(self, ctx, index: int = None):
        for server in quotes:
            if server['id'] == ctx.guild.id:

                if not server['contents']:
                    return await ctx.send('this server has no saved quotes')

                if index is None:
                    return await ctx.send(random.choice(server['contents']))

                try:
                    return await ctx.send(server['contents'][index+1])
                except IndexError:
                    return await ctx.send('this server does not have a quote of that index')

        quotes.append({
            'id': ctx.guild.id,
            'contents': [

            ]
        })
        json.dump(quotes, open('cogs/store/quotes.json', 'w'), indent = 4)
        await ctx.invoke(self.bot.get_command("quote"))

    @quote.command(name = "add")
    async def _quote_add(self, ctx, *, content: str):
        for server in quotes:
            if server['id'] == ctx.guild.id:
                server['contents'].append(content)
                json.dump(quotes, open('cogs/store/quotes.json', 'w'), indent = 4)
                return await ctx.send('added quote with an index of {}'.format(len(server['contents'])-2))

    @quote.command(name = "remove")
    async def _quote_remove(self, ctx, index: int):
        for server in quotes:
            if server['id'] == ctx.guild.id:
                try:
                    server['contents'].remove(index)
                    return await ctx.send('removed quote {}'.format(index))
                except:
                    return await ctx.send('no quote at index {}'.format(index))

    @quote.command(name = "list")
    async def _quote_list(self, ctx):
        for server in quotes:
            if server['id'] == ctx.guild.id:

                if not server['contents']:
                    return await ctx.send('this server has no quotes')

                ret = ''
                for index, item in enumerate(server['contents']):
                    ret += '{}: {}'.format(index, item)

                if len(ret) > 1900:
                    [ret[i:i+1500] for i in range(0, len(ret), 1500)]

                    for part in ret:
                        await ctx.author.send('```\n' + part + '```')

                else:
                    return await ctx.author.send('```\n' + ret + '```')


def setup(bot):
    bot.add_cog(Utility(bot))
