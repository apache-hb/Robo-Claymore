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
            rest_port=2332,
            ws_port=2333
        )

    def cog_unload(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(lavalink.close())

def setup(bot):
    bot.add_cog(Music(bot))