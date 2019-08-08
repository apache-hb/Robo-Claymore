import discord
from discord.ext import commands
from claymore import Wheel

class Reminders(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name = 'remind')
    async def _remind(self, ctx, *, txt: str):
        pass

def setup(bot):
    bot.add_cog(Reminders(bot))