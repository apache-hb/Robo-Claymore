import discord
import asyncio
import json
from discord.ext import commands
import youtube_dl
from .store import try_file

youtube_dl.utils.bug_reports_message = lambda: ''

yt_format = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_format = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(yt_format)


#Ok not gonna lie here, this code was basically stolen line for line from the music bot example
#you know i had to do it to em
'''
⠀⠀⠀⠀⣠⣦⣤⣀
⠀⠀⠀⠀⢡⣤⣿⣿
⠀⠀⠀⠀⠠⠜⢾⡟
⠀⠀⠀⠀⠀⠹⠿⠃⠄
⠀⠀⠈⠀⠉⠉⠑⠀⠀⠠⢈⣆
⠀⠀⣄⠀⠀⠀⠀⠀⢶⣷⠃⢵
⠐⠰⣷⠀⠀⠀⠀⢀⢟⣽⣆⠀⢃
⠰⣾⣶⣤⡼⢳⣦⣤⣴⣾⣿⣿⠞
⠀⠈⠉⠉⠛⠛⠉⠉⠉⠙⠁
⠀⠀⡐⠘⣿⣿⣯⠿⠛⣿⡄
⠀⠀⠁⢀⣄⣄⣠⡥⠔⣻⡇
⠀⠀⠀⠘⣛⣿⣟⣖⢭⣿⡇
⠀⠀⢀⣿⣿⣿⣿⣷⣿⣽⡇
⠀⠀⢸⣿⣿⣿⡇⣿⣿⣿⣇
⠀⠀⠀⢹⣿⣿⡀⠸⣿⣿⡏
⠀⠀⠀⢸⣿⣿⠇⠀⣿⣿⣿
⠀⠀⠀⠈⣿⣿⠀⠀⢸⣿⡿
⠀⠀⠀⠀⣿⣿⠀⠀⢀⣿⡇
⠀⣠⣴⣿⡿⠟⠀⠀⢸⣿⣷
⠀⠉⠉⠁⠀⠀⠀⠀⢸⣿⣿⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈'''
#does this seem unproffesional?
#https://github.com/Rapptz/discord.py/blob/rewrite/examples/basic_voice.py
#from there
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source,volume)

        self.data = data
        self.title = data.get('url')
        self.url = data.get('url')

    @classmethod
    async def from_url(self, url, *, loop = None, stream = False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return self(discord.FFmpegPCMAudio(filename, **ffmpeg_format), data = data)

class Song:
    pass

class Playlist:
    pass

class Voice:
    def __init__(self, bot):
        self.bot = bot
        self.queues = []
        self.user_playlists = json.load(try_file('cogs/store/playlist.json'))
        print('cog {} loaded'.format(self.__class__.__name__))

    @commands.group(invoke_without_command = True)
    async def playlist(self, ctx):
        pass

    @playlist.command(name = "add")
    async def _playlist_add(self, ctx, *links: str):
        pass

    @playlist.command(name = "remove")
    async def _playlist_remove(self, ctx, index: int = None):
        pass

    @playlist.command(name = "set")
    async def _playlist_set(self, ctx, index: int, url: str):
        pass

    @playlist.command(name = "clear")
    async def _playlist_clear(self, ctx):
        pass

    @playlist.command(name = "start")
    async def _playlist_start(self, ctx, index: int = 0):
        pass

    @playlist.command(name = "shuffle")
    async def _playlist_shuffle(self, ctx):
        pass

    @commands.command(name = "join")
    async def _join(self, ctx):
        channel = ctx.author.voice.channel

        if channel is None:
            return await ctx.send('You need to be in a voice channel')

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name = "play")
    async def _play(self, ctx, *, url: str):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop = self.bot.loop, stream = True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('now playing {}'.format(player.title))

    @commands.command(name = "volume")
    async def _volume(self, ctx, new_volume: int):
        ctx.voice_client.source.volume = new_volume
        await ctx.send('changed volume to {}'.format(new_volume))

    @commands.command(name = "stop")
    async def _stop(self, ctx):
        await ctx.voice_client.disconnect()

    @_play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('you\'re not connected to a voice channel')
                raise commands.errors.CheckFailure('no voice channel')

def setup(bot):
    bot.add_cog(Voice(bot))
