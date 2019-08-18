from claymore import Wheel
import discord
from discord.ext import commands
import asyncio
import lavalink

class Music(Wheel):
    def __init__(self, bot):
        super().__init__(bot)
        bot.add_listener(self.music_ready, 'on_ready')

    async def music_ready(self):
        await lavalink.initialize(
            self.bot,
            host='localhost',
            password='lavalink_claymore',
            rest_port=2333,
            ws_port=2333
        )
        self.bot.log.info('Initialized lavalink connection')

    @commands.command(
        name = 'join', 
        aliases = [ 'summon' ]
    )
    @commands.guild_only()
    async def _join(self, ctx):
        pass

    @commands.command(name = 'play')
    @commands.guild_only()
    async def _play(self, ctx, *, song: str):
        player = await lavalink.connect(ctx.author.voice.channel)
        tracks = await player.search_yt(song)
        player.add(ctx.author, tracks.tracks[0])
        await player.play()

    @commands.command(name = 'skip')
    @commands.guild_only()
    async def _skip(self, ctx, count: int = 1):
        pass

    @commands.command(name = 'queue')
    @commands.guild_only()
    async def _queue(self, ctx):
        pass

    @commands.command(name = 'leave')
    @commands.guild_only()
    async def _leave(self, ctx):
        player = lavalink.get_player(ctx.guild.id)
        await player.disconnect()

    def cog_unload(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(lavalink.close())

def setup(bot):
    bot.add_cog(Music(bot))