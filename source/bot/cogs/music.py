from claymore import Wheel, PagedEmbed
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

    async def add_track(self, ctx, track):
        player = await lavalink.connect(ctx.author.voice.channel)
        player.add(ctx.author, track)

        embed = ctx.make_embed(track.title, f'Requested by {ctx.author.mention}')
        embed.url = track.uri
        embed.set_thumbnail(url = track.thumbnail)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        mil = track.length
        embed.set_footer(text = f'Track is {lavalink.utils.format_time(mil)} long')

        await ctx.send(embed = embed)

    @commands.command(
        name = 'join',
        aliases = [ 'summon' ]
    )
    @commands.guild_only()
    async def _join(self, ctx):
        await lavalink.connect(ctx.author.voice.channel)
        await ctx.send(embed = ctx.make_embed('Player', 'Joined channel'))

    @commands.command(name = 'play')
    @commands.guild_only()
    async def _play(self, ctx, *, song: str):
        player = await lavalink.connect(ctx.author.voice.channel)
        tracks = await player.search_yt(song)
        song = tracks.tracks[0]

        await self.add_track(ctx, song)

        if not player.is_playing:
            await player.play()

    @commands.command(name = 'stop')
    @commands.guild_only()
    async def _stop(self, ctx):
        try:
            player = lavalink.get_player(ctx.guild.id)
        except KeyError:
            return await ctx.send(embed = ctx.make_embed('Player', 'Currently not connected to channel'))

        await player.stop()
        await ctx.send(embed = ctx.make_embed('Player', 'Stopped playing'))

    @commands.command(name = 'pause')
    @commands.guild_only()
    async def _pause(self, ctx):
        player = lavalink.get_player(ctx.guild.id)
        if player.paused:
            return await ctx.send(embed = ctx.make_embed('Player', 'Music is already paused'))

        await player.pause()
        await ctx.send(embed = ctx.make_embed('Player', 'Music has been paused'))

    @commands.command(name = 'resume')
    @commands.guild_only()
    async def _resume(self, ctx):
        player = lavalink.get_player(ctx.guild.id)
        if player.paused:
            await player.pause(False)
            await ctx.send(embed = ctx.make_embed('Player', 'Resumed music'))
        else:
            await ctx.send(embed = ctx.make_embed('Player', 'Player is not paused'))

    @commands.command(name = 'volume')
    @commands.guild_only()
    async def _volume(self, ctx, volume: int = None):
        player = lavalink.get_player(ctx.guild.id)

        if volume is None:
            return await ctx.send(embed = ctx.make_embed('Player', f'Volume is currently {player.volume}'))

        if volume not in range(0, 150):
            return await ctx.send(embed = ctx.make_embed('Player', 'Volume must be between 0 and 150'))

        await player.set_volume(volume)
        await ctx.send(embed = ctx.make_embed('Player', f'Volume has been set to {volume}'))

    @commands.command(name = 'skip')
    @commands.guild_only()
    async def _skip(self, ctx, count: int = 1):
        try:
            player = lavalink.get_player(ctx.guild.id)
        except KeyError:
            return await ctx.send(embed = ctx.make_embed('Player', 'Not currently connected to channel'))

        await player.skip()
        await ctx.send(embed = ctx.make_embed('Player', 'Skipped song'))

    @commands.command(name = 'queue')
    @commands.guild_only()
    async def _queue(self, ctx):
        try:
            player = lavalink.get_player(ctx.guild.id)
        except KeyError:
            return await ctx.send(embed = ctx.make_embed('Player', 'Not currently connected'))

        tracks = player.queue

        if not tracks:
            return await ctx.send(embed = ctx.make_embed('Player', 'No tracks currently in queue'))

        embed = PagedEmbed('Player', 'Current tracks')

        for track in tracks:
            embed.add_field(track.title, f'Requested by {track.requester.mention}', inline = False)

        await ctx.send_pages(embed)

    @commands.command(
        name = 'current',
        aliases = [ 'nowplaying', 'now', 'np' ]
    )
    @commands.guild_only()
    async def _current(self, ctx):
        try:
            player = lavalink.get_player(ctx.guild.id)
        except KeyError:
            return await ctx.send(embed = ctx.make_embed('Player', 'Not currently connected'))

        track = player.current
        embed = ctx.make_embed(f'Now playing {track.title}', f'Requested by {track.requester.mention}')
        embed.set_thumbnail(url = track.thumbnail)
        embed.set_footer(
            text = f'{lavalink.utils.format_time(player.position)}/{lavalink.utils.format_time(track.length)}'
        )

        await ctx.send(embed = embed)

    @commands.command(name = 'leave')
    @commands.guild_only()
    async def _leave(self, ctx):
        try:
            player = lavalink.get_player(ctx.guild.id)
        except KeyError:
            return await ctx.send(embed = ctx.make_embed('Player', 'Already disconnected from channel'))

        await player.disconnect()
        await ctx.send(embed = ctx.make_embed('Player', 'Player has disconnected from channel'))

    def cog_unload(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(lavalink.close())

def setup(bot):
    bot.add_cog(Music(bot))