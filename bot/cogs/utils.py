from discord.ext.commands import command
from claymore.utils import wheel, Context
from claymore.claymore import Claymore

class Utils(wheel(desc = 'helpful tools')):
    @command()
    async def ping(self, ctx: Context):
        await ctx.send(f'Pong {self.bot.latency*1000:.0f}ms')

def setup(bot: Claymore):
    bot.add_cog(Utils(bot))
