from discord.ext.commands import command
from claymore.utils import wheel, Context
from claymore.claymore import Claymore

from random import choice
from textwrap import dedent

class Utils(wheel(desc = 'helpful tools')):
    @command()
    async def ping(self, ctx: Context):
        await ctx.send(f'Pong {self.bot.latency*1000:.0f}ms')

    @command()
    async def randomcase(self, ctx, *, text: str):
        await ctx.send(''.join(choice((str.upper, str.lower))(c) for c in text))

    @command()
    async def invite(self, ctx):
        fields = { 'invite': f'[invite me to your server](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8)' }
        server = self.bot.config['discord']['invite'] or None
        if server:
            fields['support'] = f'[join the support server]({server})'

        await ctx.send(embed = ctx.embed(
            'invite', 'invite me to your server', fields,
            thumbnail = self.bot.user.avatar_url
        ))

def setup(bot: Claymore):
    bot.add_cog(Utils(bot))
