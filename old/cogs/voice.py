import discord
import asyncio
import json
from discord.ext import commands
import youtube_dl
from .utils.shortcuts import try_file
from typing import Union, List
#TODO redo all the stuff here as well
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
    def __init__(self, source, *, data, volume: int = 0.5):
        super().__init__(source, volume)

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
    def __init__(self, url, thumbnail, user: discord.Member):
        self.url = url
        self.thumbnail = thumbnail
        self.requester = user

    def make_embed(self) -> discord.Embed:
        pass

#make a song by searching for a url
#raises LookupError if no song is found
async def search_url(url: str) -> Song:
    print(url)
    raise NotImplementedError()

class Playlist:
    def __init__(self, song: Union[Song, List[Song]]):
        self.volume = 50
        if isinstance(song, list):
            self.songs = song
        else:
            self.songs = [song]

    def set_volume(self, new: int):
        if new not in range(0, 100):
            raise IndexError()
        self.volume = new

    def next(self) -> Song:
        return self.songs.pop()

    def skip(self):
        self.songs.pop()

    def remove(self, index: int):
        self.songs.remove(index)

    def add_song(self, song: Song):
        self.songs.append(song)

    def make_embed(self) -> discord.Embed:
        if not self.songs:
            return discord.Embed(title = 'No songs left')
        embed = discord.Embed(title = 'Songs in queue')
        embed.description = f'there are {len(self.songs)} song(s) left in the queue'
        for song in self.songs:
            embed.add_field(name = song.name, value = f'Requested by {song.requester.name}')

    def currently_playing(self) -> discord.Embed:
        return self.songs[0]

    def serialize(self):
        r = [{'requester': each.requester.name, 'url': each.url} for each in self.songs]
        return json.dumps(r)

#TODO all of this
class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = []
        self.user_playlists = json.load(try_file('cogs/store/playlist.json'))
        print(f'cog {self.__class__.__name__} loaded')

    @commands.group(
        invoke_without_command = True,
        case_insensitive = True
    )
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
        channel: discord.TextChannel = ctx.author.voice.channel

        if channel is None:
            return await ctx.send('You need to be in a voice channel')

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name = "play")
    async def _play(self, ctx, *, url: str):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop = self.bot.loop, stream = True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'now playing {player.title}')

    @commands.command(name = "volume")
    async def _volume(self, ctx, new_volume: int):
        ctx.voice_client.source.volume = new_volume
        await ctx.send(f'changed volume to {new_volume}')

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
