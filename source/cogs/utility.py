import discord
from discord.ext import commands

from itertools import chain
from urllib.parse import urlencode
from xml.etree import ElementTree as ET
import aiohttp
import json
from random import choice, randint
from .store import Store, style_embed, shorten_url, pyout, dir_path
from datetime import datetime
import platform

#wikia fandom wikis
WIKIA_API_URL = 'http://{lang}{sub_wikia}.wikia.com/api/v1/{action}'
WIKIA_STANDARD_URL = 'http://{lang}{sub_wikia}.wikia.com/wiki/{page}'
WIKIPEDIA_API_URL = 'http://en.wikipedia.org/w/api.php'

USER_AGENT = '{type} (https://github.com/Apache-HB/Robo-Claymore)'

#stolen from appuselfbot 
#https://github.com/appu1232/Discord-Selfbot
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
        pyout('Wolfram loaded')

    async def query(self, question, params=(), **kwargs):
        data = dict(
            input=question,
            appid=self.key
        )
        data = chain(params, data.items(), kwargs.items())
        query = urlencode(tuple(data))
        url = 'https://api.wolframalpha.com/v2/query?' + query
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return ET.fromstring(await resp.text())

class Zalgo:

    def __init__(self, txt: str, intensity: int):
        self.txt = txt
        self.intensity = intensity

    def __str__(self):
        return self.zalgo(text=self.txt, intensity=self.intensity).decode('utf-8')

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
            zalgo_num = randint(0, zalgo_threshold) + 1
            for _ in range(zalgo_num):
                zalgoized.append(choice(zalgo_chars))
        response = choice(zalgo_chars).join(zalgoized)
        return response.encode('utf8', 'ignore')


    def _insert_randoms(self, text):
        random_extras = [chr(i) for i in range(0x1D023, 0x1D045 + 1)]
        newtext = []
        for char in text:
            newtext.append(char)
            if randint(1, 5) == 1:
                newtext.append(choice(random_extras))
        return u''.join(newtext)

    def _is_narrow_build(self):
        try:
            chr(0x10000)
        except ValueError:
            return True
        return False

class Utility:
    def __init__(self, bot):
        self.bot = bot
        self.a = 0
        self.wolfram = Wolfram(Store.config['wolfram']['key'])
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Miscellaneous functions"
    description = "For extra\'s that don\'t fit in"
    hidden = True

    @commands.command(name="randomcase")
    async def _randomcase(self, ctx, *, message: str):
        await ctx.send(''.join(choice((str.upper,str.lower))(x) for x in message))

    @commands.command(name="zalgo")
    async def _zalgo(self, ctx, *, text: str=None):
        text = text.split(' ')
        try:
            intensity = int(text[-1])
        except Exception:
            intensity = 50
            text = ' '.join(text)
        else:
            text = ' '.join(text[:-1])
        
        try:
            await ctx.send(Zalgo(txt=text , intensity=intensity))
        except Exception:
            await ctx.send('Cannot zalgo this much text, this is discords fault, not mine')

    @commands.command(name="emoji")
    async def _emoji(self, ctx, *, text: str=None):
        if text is None:
            text = 'bottom text'
        
        ret=''
        for letter in text.lower():
            try:
                ret+=emoji_dict[str(letter)][0]
            except Exception:
                ret+=emoji_dict[' '][0]
        
        try:
            await ctx.send(ret)
        except Exception:
            await ctx.send('Cannot emojify that much text, this is discords fault, not mine')

    @commands.command(name="square")
    async def _square(self, ctx, *, text: str=None):
        if text is None:
            text = 'bottom text'

        ret = text + '\n'
        for letter in text:
            ret+=letter+'\n'
        try:
            await ctx.send(ret)
        except Exception:
            await ctx.send('Cannot square this much text, this is discords fault, not mine')

    @commands.command(name="urban")
    async def _urban(self, ctx, search: str=None):
        if search is None:
            url = 'http://api.urbandictionary.com/v0/random'
        else:
            url = 'http://api.urbandictionary.com/v0/define?term=' + search
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                j = json.loads(await resp.text())

                if not j['list']:
                    return await ctx.send('Nothing called {} found'.format(search))

                while True:
                    try:
                        post = j['list'][self.a]
                        self.a+=1
                        break
                    except Exception:
                        self.a = 0
                        post = j['list'][self.a]
                        break

                embed=style_embed(ctx, title='Definition of {}'.format(post['word']),
                description='Posted by {}'.format(post['author']))
                embed.add_field(name='Description', value=post['definition'])
                embed.add_field(name='Example', value=post['example'])
                embed.add_field(name='Permalink', value=post['permalink'])
                embed.set_footer(text='Votes: {up}/{down}'.format(
                    up=post['thumbs_up'],
                    down=post['thumbs_down']
                ))
                await ctx.send(embed=embed)

    @commands.command(name="credits", aliases=['credit'])
    async def _credits(self, ctx):
        pass

    @commands.command(name="userinfo",
    aliases=['memberinfo', 'playerinfo', 'aboutuser'])
    async def _userinfo(self, ctx, user: discord.Member=None):
        if user is None:
            user = ctx.message.author
        embed=style_embed(ctx, title='Info about {}'.format(
            user.name+'#'+user.discriminator+' - ('+user.display_name+')'
        ), description='ID: {}'.format(user.id))
        embed.set_thumbnail(url=user.avatar_url)
        now = datetime.now()
        diffrence = now - user.joined_at
        embed.add_field(name='Time spent in {}'.format(ctx.guild.name), 
        value='First joined at {}, thats {} days ago'.format(user.joined_at.date(), diffrence.days), inline=False)
        diffrence = now - user.created_at
        embed.add_field(name='Time spent on discord', value='First signed up at {}, thats over {} days ago'.format(
            user.created_at.date(), diffrence.days
        ), inline=False)
        roles = []
        for a in user.roles:
            roles.append(a.name)
        embed.add_field(name='Roles', value=', '.join(roles))
        embed.add_field(name='Is a bot', value=user.bot)
        await ctx.send(embed=embed)
        

    @commands.command(name="selfinfo", aliases=['me'])
    async def _selfinfo(self, ctx):
        await ctx.invoke(ctx.bot.get_command("userinfo"))

    @commands.command(name="serverinfo")
    async def _serverinfo(self, ctx):
        embed=style_embed(ctx, title='Server information about {}'.format(ctx.guild.name),
        description='ID: {}'.format(ctx.guild.id))
        now = datetime.now()
        diffrence = now - ctx.guild.created_at
        embed.add_field(name='Created at', value='{}, thats over {} days ago'.format(
            ctx.guild.created_at.date(),
            diffrence.days
        ), inline=False)
        embed.add_field(name='User Count', value=len(ctx.guild.members))
        embed.add_field(name='Owner', value=ctx.guild.owner.name)
        embed.add_field(name='Text channels', value=len(ctx.guild.text_channels))
        embed.add_field(name='Voice channels', value=len(ctx.guild.voice_channels))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="botinfo")
    async def _botinfo(self, ctx):
        embed=style_embed(ctx, title='Info about me, {}'.format(ctx.bot.user.name))
        embed.add_field(name='Working directory', value=dir_path)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='discord.py version', value=discord.__version__)
        embed.add_field(name='bot name and id', value="Name: {name}, ID: {id}".format(id=self.bot.user.id, name=self.bot.user.name))
        embed.add_field(name='Architecture', value=platform.machine())
        embed.add_field(name='Version', value=platform.version())
        embed.add_field(name='Platform', value=platform.platform())
        embed.add_field(name='Processor', value=platform.processor())
        await ctx.send(embed=embed)

    @commands.command(name="wikipedia")
    async def _wikipedia(self, ctx, *, search: str):
        params = {
            'action': 'Search/List?/',
            'lang': 'en',
            'limit': 10,
            'query': search
        }
        api_url = WIKIPEDIA_API_URL.format(**params)



    @commands.command(name="wikia")
    async def _wikia(self, ctx, subwiki: str, *, search: str):
        params = {
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
                print(await resp.text())

    @commands.command(name="wolfram")
    async def _wolfram(self, ctx, *, query: str=None):
        root = await self.wolfram.query(query)
        for child in root:
            if child.attrib['scanner'] == 'Simplification':
                for subobject in child:
                    for subsubobject in subobject:
                        if subsubobject.tag == 'plaintext':
                            embed=style_embed(ctx, title='From wolfram alpha',
                            description='Awnser to the question {}'.format(query))
                            embed.add_field(name='Awnser', value=subsubobject.text)
                            return await ctx.send(embed=embed)

    @commands.command(name="shorten")
    async def _shorten(self, ctx, *, url: str=None):
        if not url is None:
            return await ctx.send(await shorten_url(long_url=url))
        return await ctx.send('You need to enter a url')

def setup(bot):
    bot.add_cog(Utility(bot))