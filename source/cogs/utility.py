import discord
from discord.ext import commands

from itertools import chain
from urllib.parse import urlencode
from defusedxml.ElementTree import fromstring
import xml.dom.minidom
import aiohttp
import json
import unicodedata
from bs4 import BeautifulSoup
import random

from .utils import quick_embed, shorten_url, is_emoji

from .store import (config, quotes, tags, whitelist, blacklist)

from inspect import getsource
from datetime import datetime
import time
import platform

# wikia fandom wikis
WIKIA_API_URL = 'http://{lang}{sub_wikia}.wikia.com/api/v1/{action}'
WIKIA_STANDARD_URL = 'http://{lang}{sub_wikia}.wikia.com/wiki/{page}'
WIKIPEDIA_API_URL = 'http://en.wikipedia.org/w/api.php'

USER_AGENT = '{type} (https://github.com/Apache-HB/Robo-Claymore)'

# stolen from appuselfbot
# https://github.com/appu1232/Discord-Selfbot
emoji_dict = {
    'a': ['🇦 ', '🅰', '🍙', '🔼', '4⃣'],
    'b': ['🇧 ', '🅱', '8⃣'],
    'c': ['🇨 ', '©', '🗜'],
    'd': ['🇩 ', '↩'],
    'e': ['🇪 ', '3⃣', '📧', '💶'],
    'f': ['🇫 ', '🎏'],
    'g': ['🇬 ', '🗜', '6⃣', '9⃣', '⛽'],
    'h': ['🇭 ', '♓'],
    'i': ['🇮 ', 'ℹ', '🚹', '1⃣'],
    'j': ['🇯 ', '🗾'],
    'k': ['🇰 ', '🎋'],
    'l': ['🇱 ', '1⃣', '🇮', '👢', '💷'],
    'm': ['🇲 ', 'Ⓜ', '📉'],
    'n': ['🇳 ', '♑', '🎵'],
    'o': ['🇴 ', '🅾', '0⃣', '⭕', '🔘', '⏺', '⚪', '⚫', '🔵', '🔴', '💫'],
    'p': ['🇵 ', '🅿'],
    'q': ['🇶 ', '♌'],
    'r': ['🇷 ', '®'],
    's': ['🇸 ', '💲', '5⃣', '⚡', '💰', '💵'],
    't': ['🇹 ', '✝', '➕', '🎚', '🌴', '7⃣'],
    'u': ['🇺 ', '⛎', '🐉'],
    'v': ['🇻 ', '♈', '☑'],
    'w': ['🇼 ', '〰', '📈'],
    'x': ['🇽 ', '❎', '✖', '❌', '⚒'],
    'y': ['🇾 ', '✌', '💴'],
    'z': ['🇿 ', '2⃣'],
    '0': ['0⃣ ', '🅾', '0⃣', '⭕', '🔘', '⏺', '⚪', '⚫', '🔵', '🔴', '💫'],
    '1': ['1⃣ ', '🇮'],
    '2': ['2⃣ ', '🇿'],
    '3': ['3⃣ '],
    '4': ['4⃣ '],
    '5': ['5⃣ ', '🇸', '💲', '⚡'],
    '6': ['6⃣ '],
    '7': ['7⃣ '],
    '8': ['8⃣ ', '🎱', '🇧', '🅱'],
    '9': ['9⃣ '],
    '?': ['❓ '],
    '!': ['❗ ', '❕', '⚠', '❣'],
    ' ': ['   '],
    '\n': ['\n']
}


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
        return self.zalgo(
            text=self.txt, intensity=self.intensity).decode('utf-8')

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
        self.loop = 0
        self.wolfram = Wolfram(config['wolfram']['key'])
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Miscellaneous functions"
    description = "For extra\'s that don\'t fit in"

    @commands.command(name="source")
    async def _source(self, ctx, *, command: str):
        func = ctx.bot.get_command(command).callback
        try:
            await ctx.send('```py\n' + getsource(func) + '\n```')
        except OSError:
            await ctx.send('Code could not be retrived')
        except Exception:
            await ctx.send('The source for that command is too big to send')

    # TODO: figure out why this doesnt work

    @commands.command(name="hastebin", hidden=True)
    async def _hastebin(self, ctx, *, message: str):
        async with aiohttp.ClientSession() as session:  # TODO test this
            async with session.post(
                    'https://hastebin.com/documents',
                    data=message.encode('utf-8')) as resp:
                await ctx.send(await resp.text() + await resp.json()['key'])

    @commands.command(name="findreplace")
    async def _findreplace(self, ctx, find: str, replace: str, *,
                           message: str):
        try:
            await ctx.send(message.replace(find, replace))
        except Exception:
            await ctx.send('I cannot find and replace that')

    # TODO a hell of alot of testing
    @commands.command(name="togif", hidden=True)
    async def _togif(self, ctx, duration: int, *, message: str):
        images = []
        message = message.split(' ').split('\n')
        async with aiohttp.ClientSession() as session:
            for link in message:
                async with session.get(link) as resp:
                    images.append(imageio.imread(await resp.text()))
        imageio.mimsave('temp.gif', images)
        await ctx.send(file=discord.File(open('temp.gif')))

    @commands.command(name="charinfo")
    async def _charinfo(self, ctx, *, message: str):
        ret = ''
        for a in message[:5]:
            ret += '``{}`` is ``{}`` in unicode\n'.format(
                a, unicodedata.name(a))
        await ctx.send(ret)

    @commands.command(name="randomcase")
    async def _randomcase(self, ctx, *, message: str):
        await ctx.send(''.join(
            random.choice((str.upper, str.lower))(x) for x in message))

    @commands.command(name="zalgo")
    async def _zalgo(self, ctx, *, text: str = None):
        text = text.split(' ')
        try:
            intensity = int(text[-1])
        except Exception:
            intensity = 50
            text = ' '.join(text)
        else:
            text = ' '.join(text[:-1])

        try:
            await ctx.send(Zalgo(txt=text, intensity=intensity))
        except Exception:
            await ctx.send(
                'Cannot zalgo this much text, this is discords fault, not mine'
            )

    @commands.command(name="emoji")
    async def _emoji(self, ctx, *, text: str = None):
        if text is None:
            text = 'bottom text'

        ret = ''
        for letter in text.lower():
            try:
                ret += emoji_dict[str(letter)][0]
            except Exception:
                ret += emoji_dict[' '][0]

        try:
            await ctx.send(ret)
        except Exception:
            await ctx.send(
                'Cannot emojify that much text, this is discords fault, not mine'
            )

    @commands.command(name="square")
    async def _square(self, ctx, *, text: str = None):
        if text is None:
            text = 'bottom text'

        ret = text + '\n'
        for letter in text:
            ret += letter + '\n'
        try:
            await ctx.send(ret)
        except Exception:
            await ctx.send(
                'Cannot square this much text, this is discords fault, not mine'
            )

    @commands.command(name="reverse")
    async def _reverse(self, ctx, *, message: str):
        await ctx.send(message[::-1])

    @commands.command(name="invert")
    async def _invert(self, ctx, *, message: str):
        await ctx.send(message.swapcase())

    @commands.command(name="binary")
    async def _binary(self, ctx, *, message: str):
        try:
            await ctx.send(' '.join(format(ord(x), 'b') for x in message))
        except Exception as e:
            print(e)
            await ctx.send('Cannot send this much binary, blame b1nzy for this'
                           )

    @commands.command(name="ascii")
    async def _ascii(self, ctx, *, message: str):
        try:
            await ctx.send(''.join(str([ord(c) for c in message])))
        except Exception as e:
            print(e)
            await ctx.send(
                'Cannot send that much ascii, blame b1nzy, this is his fault')

    @commands.group(invoke_without_command=True)
    async def prettyprint(self, ctx):
        pass

    @prettyprint.command(name="json")
    async def _prettyprint_json(self, ctx, *, message: str):
        try:
            ret = json.loads(message)
            await ctx.send('```json\n' + json.dumps(ret, indent=4) + '```')
        except json.JSONDecodeError:
            await ctx.send('Cannot print malformed json')

    @prettyprint.command(name="xml")
    async def _prettyprint_xml(self, ctx, *, message: str):
        try:
            ret = xml.dom.minidom.parseString(message)
            await ctx.send('```xml\n' + ret.toprettyxml() + '```')
        except Exception:
            await ctx.send('Cannot pretty print malformed xml')

    @prettyprint.command(name="html")
    async def _prettyprint_html(self, ctx, *, message: str):
        try:
            await ctx.send('```html\n' + BeautifulSoup(message, 'html.parser')
                           .prettify() + '```')
        except Exception:
            await ctx.send('Cannot print malformed html')

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def autoreact(self, ctx):
        embed = quick_embed(ctx, title='All subcommands for autoreact')
        c = []
        for a in self.looputoreact.walk_commands():
            if a.name not in c:  # prevent duplicates
                embed.add_field(name=a.name, value=a.brief)
            c.append(a.name)
        await ctx.send(embed=embed)

    @autoreact.command(name="add")
    @commands.guild_only()
    async def _autoreact_add(self, ctx, *, message: str):
        message = message.split(' ')
        react = message[-1]
        if not is_emoji(react):
            return await ctx.send('That is not an emoji I can react with')
        phrase = ' '.join(message[:-1])
        ret = {
            "phrase": phrase.lower(),
            "react": react,
            "meta": {
                "time_created": int(time.time()),
                "created_by": ctx.author.id,
                "created_in": ctx.channel.id,
                "uses": 0
            }
        }
        for a in autoreact:
            if a['server_id'] == ctx.guild.id:
                a['contents'].append(ret)
        json.dump(autoreact, open('cogs/store/autoreact.json', 'w'), indent=4)
        await ctx.send('``{}`` is now reacted to with ``{}``'.format(
            phrase, react))

    @autoreact.command(name="remove", aliases=['delete', 'subtract'])
    @commands.guild_only()
    async def _autoreact_remove(self, ctx, *, message: str):
        message = message.split(' ')
        react = message[-1]
        phrase = ' '.join(message[:-1])

        for a in autoreact:
            if a['server_id'] == ctx.guild.id:
                for b in a['contents']:
                    if b['phrase'].lower() == phrase.lower(
                    ) and b['react'] == react:
                        a['contents'].remove(b)
                        json.dump(
                            autoreact,
                            open('cogs/store/autoreact.json', 'w'),
                            indent=4)
                        return await ctx.send('Autoreact removed')
        await ctx.send('No Autoreact found')

    @autoreact.command(name="purge")
    @commands.guild_only()
    async def _autoreact_purge(self, ctx):
        if not (ctx.guild.owner == ctx.author
                or self.bot.is_owner(ctx.author.id)):
            return await ctx.send('You must be the guild owner to do this')

        for a in autoreact:
            if a['server_id'] == ctx.guild.id:
                del a['contents'][:]
        json.dump(autoreact, open('cogs/store/autoreact.json', 'w'), indent=4)
        await ctx.send('Autoreacts purged for this guild')

    @autoreact.command(name="info")
    @commands.guild_only()
    async def _autoreact_info(self, ctx, *, message: str):
        message = message.split(' ')
        react = message[-1]
        phrase = ' '.join(message[:-1])

        for a in autoreact:
            if a['server_id'] == ctx.guild.id:
                for b in a['contents']:
                    if b['phrase'].lower() == phrase.lower(
                    ) and b['react'] == react:
                        embed = quick_embed(ctx, title='Autoreact info')
                        embed.add_field(
                            name='Times used', value=str(b['meta']['uses']))
                        embed.add_field(
                            name='Created in',
                            value=self.bot.get_channel(
                                b['meta']['created_in']).name)
                        embed.add_field(
                            name='Created by',
                            value=self.bot.get_user(
                                b['meta']['created_by']).name)
                        embed.add_field(
                            name='Time made',
                            value=str(
                                time.strftime('%Y-%m-%d %H:%M:%S',
                                              time.localtime(
                                                  b['meta']['time_created']))))
                        embed.add_field(name='Phrase', value=b['phrase'])
                        embed.add_field(name='React', value=b['react'])
                        return await ctx.send(embed=embed)
                await ctx.send('Nothing found')

    @autoreact.command(name="list")
    @commands.guild_only()
    async def _autoreact_list(self, ctx):
        ret = ''
        for server in autoreact:
            if server['server_id'] == ctx.guild.id:
                for content in server['contents']:
                    ret += '``{}`` is reacted with {}\n'.format(
                        content['phrase'], content['react'])
                break

        messages = [ret[i:i + 1500] for i in range(0, len(ret), 1500)]
        for message in messages:
            await ctx.author.send(message)
        await ctx.send('I have delivered the list to you\'re inbox')

    @commands.group(invoke_without_command=True, hidden=True)
    async def quote(self, ctx, index: int = None):
        pass

    @quote.command(name="add")
    async def _quote_add(self, ctx, name: str, *, message: str):
        pass

    @quote.command(name="remove")
    async def _quote_remove(self, ctx, index: int):
        pass

    @quote.command(name="purge")
    async def _quote_purge(self, ctx):
        pass

    @quote.command(name="list")
    async def _quote_list(self, ctx):
        pass

    @quote.command(name="info")
    async def _quote_info(self, ctx, index: int):
        pass

    @commands.group(invoke_without_command=True, hidden=True)
    @commands.guild_only()
    async def tag(self, ctx, name: str = None):
        pass

    @tag.command(name="add")
    @commands.guild_only()
    async def _tag_add(self, ctx, name: str, *, content: str):
        for a in tags:
            if a['server_id'] == ctx.guild.id:
                if any(d['name'] == name for d in a['contents']):
                    return await ctx.send('A tag with that name already exists'
                                          )

                ret = {
                    'name': name.lower(),
                    'content': content,
                    'meta': {
                        'protected': False,
                        'time_created': int(time.time()),
                        'created_by': ctx.author.id,
                        'created_in': ctx.channel.id,
                        'uses': 0
                    }
                }

                a['contents'].append(ret)
                json.dump(tags, open('cogs/store/tags.json', 'w'), indent=4)
                await ctx.send('tag ``{}`` was added'.format(name))

    @tag.command(name="remove")
    @commands.guild_only()
    async def _tag_remove(self, ctx, name: str):
        is_admin = ctx.author.permissions_in(ctx.channel).administrator

        for a in tags:
            if a['server_id'] == ctx.guild.id:
                for b in a['contents']:
                    if name.lower() == b['name']:
                        if a['meta']['protected']:
                            if ctx.author.id not in whitelist or self.bot.is_owner(
                                    ctx.author.id):
                                if not is_admin:
                                    return await ctx.send(
                                        'this tag is protected, and you don\'t have the permissions to remove it'
                                    )
                        a['contents'].remove(b)
                        json.dump(
                            tags, open('cogs/store/tags.json', 'w'), indent=4)
                        return await ctx.send(
                            'tag ``{}`` was removed'.format(name))
                await ctx.send('no tag called ``{}`` was found'.format(name))

    @tag.command(name="protect")
    @commands.guild_only()
    async def _tag_protect(self, ctx, name: str):
        if ctx.author.id not in whitelist or self.bot.is_owner(ctx.author.id):
            if not ctx.author.permissions_in(ctx.channel).administrator:
                return await ctx.send('You must be an administrator to do this'
                                      )

        for a in tags:
            if a['server_id'] == ctx.guild.id:
                for b in a['contents']:
                    if b['name'] == name.lower():
                        b['meta']['protected']
                        json.dump(
                            tags, open('cogs/store/tags.json', 'w'), indent=4)
                        return await ctx.send(
                            'the tag ``{}`` is now protected'.format(name))

    @tag.command(name="purge")
    @commands.guild_only()
    async def _tag_purge(self, ctx):
        if ctx.author.id not in whitelist or self.bot.is_owner(ctx.author.id):
            if not ctx.author.permissions_in(ctx.channel).administrator:
                return await ctx.send('You must be an administrator to do this'
                                      )

        for a in tags:
            if a['server_id'] == ctx.guild.id:
                del a['contents'][:]
                json.dump(tags, open('cogs/store/tags.json', 'w'), indent=4)
                await ctx.send('all tags have been purged')

    @tag.command(name="list")
    @commands.guild_only()
    async def _tag_list(self, ctx):
        pass

    @tag.command(name="info")
    @commands.guild_only()
    async def _tag_info(self, ctx, name: str):
        pass

    @commands.group(invoke_without_command=True, hidden=True)
    async def welcome(self, ctx):
        pass

    @welcome.command(name="set")
    async def _welcome_set(self, ctx, *, message: str = 'Hello'):
        pass

    @welcome.command(name="remove")
    async def _welcome_remove(self, ctx):
        pass

    @commands.group(invoke_without_command=True, hidden=True)
    async def leave(self, ctx):
        pass

    @leave.command(name="set")
    async def _leave_set(self, ctx, *, message: str = 'Goodbye'):
        pass

    @leave.command(name="remove")
    async def _leave_remove(self, ctx):
        pass

    @commands.command(name="urban")
    async def _urban(self, ctx, search: str = None):
        if search is None:
            url = 'http://api.urbandictionary.com/v0/random'
        else:
            url = 'http://api.urbandictionary.com/v0/define?term=' + search

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                j = json.loads(await resp.text())

                if not j['list']:
                    return await ctx.send(
                        'Nothing called {} found'.format(search))

                while True:
                    try:
                        post = j['list'][self.loop]
                        self.loop += 1
                        break
                    except Exception:
                        self.loop = 0
                        post = j['list'][self.loop]
                        break

                embed = quick_embed(
                    ctx,
                    title='Definition of {}'.format(post['word']),
                    description='Posted by {}'.format(post['author']))
                embed.add_field(name='Description', value=post['definition'])
                embed.add_field(name='Example', value=post['example'])
                embed.add_field(name='Permalink', value=post['permalink'])
                embed.set_footer(text='Votes: {up}/{down}'.format(
                    up=post['thumbs_up'], down=post['thumbs_down']))
                await ctx.send(embed=embed)

    @commands.command(
        name="userinfo", aliases=['memberinfo', 'playerinfo', 'aboutuser'])
    async def _userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        embed = quick_embed(
            ctx,
            title='Info about {}'.format(user.name + '#' + user.discriminator +
                                         ' - (' + user.display_name + ')'),
            description='ID: {}'.format(user.id))
        embed.set_thumbnail(url=user.avatar_url)
        now = datetime.now()
        diffrence = now - user.joined_at
        embed.add_field(
            name='Time spent in {}'.format(ctx.guild.name),
            value='First joined at {}, thats {} days ago'.format(
                user.joined_at.date(), diffrence.days),
            inline=False)
        diffrence = now - user.created_at
        embed.add_field(
            name='Time spent on discord',
            value='First signed up at {}, thats over {} days ago'.format(
                user.created_at.date(), diffrence.days),
            inline=False)
        roles = []
        for a in user.roles:
            roles.append(a.name)
        embed.add_field(name='Roles', value=', '.join(roles))
        embed.add_field(name='Is a bot', value=user.bot)
        await ctx.send(embed=embed)

    @commands.command(name="selfinfo", aliases=['me'])
    async def _selfinfo(self, ctx):
        await ctx.invoke(self.bot.get_command("userinfo"))

    @commands.command(name="serverinfo")
    async def _serverinfo(self, ctx):
        embed = quick_embed(
            ctx,
            title='Server information about {}'.format(ctx.guild.name),
            description='ID: {}'.format(ctx.guild.id))
        now = datetime.now()
        diffrence = now - ctx.guild.created_at
        embed.add_field(
            name='Created at',
            value='{}, thats over {} days ago'.format(
                ctx.guild.created_at.date(), diffrence.days),
            inline=False)
        embed.add_field(name='User Count', value=len(ctx.guild.members))
        embed.add_field(name='Owner', value=ctx.guild.owner.name)
        embed.add_field(
            name='Text channels', value=len(ctx.guild.text_channels))
        embed.add_field(
            name='Voice channels', value=len(ctx.guild.voice_channels))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="botinfo")
    async def _botinfo(self, ctx):
        embed = quick_embed(
            ctx, title='Info about me, {}'.format(self.bot.user.name))
        embed.add_field(name='Working directory', value=dir_path)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='discord.py version', value=discord.__version__)
        embed.add_field(
            name='bot name and id',
            value="Name: {name}, ID: {id}".format(
                id=self.bot.user.id, name=self.bot.user.name))
        embed.add_field(name='Architecture', value=platform.machine())
        embed.add_field(name='Version', value=platform.version())
        embed.add_field(name='Platform', value=platform.platform())
        embed.add_field(name='Processor', value=platform.processor())
        await ctx.send(embed=embed)

    @commands.command(name="wikipedia")
    async def _wikipedia(self, ctx, *, search: str):
        '''params = {
            'action': 'Search/List?/',
            'lang': 'en',
            'limit': 10,
            'query': search
        }
        api_url = WIKIPEDIA_API_URL.format(**params)'''

    @commands.command(name="wikia")
    async def _wikia(self, ctx, subwiki: str, *, search: str):
        '''params = {
            'action': 'Search/List?/',
            'sub_wikia': subwiki,
            'lang': 'en',
            'limit': 10,
            'query': search
        }

        api_url = WIKIA_API_URL.format(**params)
        params['format'] = 'json'
        headers = {
            'User-Agent': USER_AGENT.format('wikia')
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params, headers=headers) as resp:
                print(await resp.text())'''

    @commands.command(name="hash")
    async def _hash(self, ctx, *, seed: str):
        await ctx.send(hash(seed))

    NASA_URL = 'https://images-api.nasa.gov/search?q={search}'

    @commands.command(name="nasa")
    async def _nasa(self, ctx, *, search: str = 'hubble'):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.NASA_URL.format(search=search)) as resp:
                j = json.loads(await resp.text())
                if not j['collection']['items']:
                    return await ctx.send(
                        'Nothing found for the search {}'.format(search))
                try:
                    a = j['collection']['items'][self.loop]
                except IndexError:
                    self.loop = 0
                    a = j['collection']['items'][self.loop]

                embed = quick_embed(
                    ctx,
                    title=a['data'][0]['title'],
                    description='Created at {}'.format(
                        a['data'][0]['date_created']))
                async with session.get(a['href']) as resp:
                    z = json.loads(await resp.text())
                    if is_embedable(z[0]):
                        embed.set_image(url=z[0])
                await ctx.send(embed=embed)

    # TODO make this nice
    @commands.command(name="wolfram")
    async def _wolfram(self, ctx, *, query: str):
        if config['wolfram']['key'] == '':
            return await ctx.send('Wolfram has not been setup on this bot')
        embed=quick_embed(ctx, title='Possible awnsers to {}'.format(query),
        description='From wolfram alpha')
        root = await self.wolfram.query(query)
        for child in root:
            for subobject in child:
                for subsubobject in subobject:
                    if subsubobject.tag == 'plaintext':
                        embed.add_field(name='Possible awnser', value=subsubobject.text)
                        return await ctx.send(embed=embed)

    @commands.command(name="shorten")
    async def _shorten(self, ctx, *, url: str):
        await ctx.send(await shorten_url(long_url=url))


def setup(bot):
    bot.add_cog(Utility(bot))
