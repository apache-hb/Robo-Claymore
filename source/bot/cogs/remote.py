from claymore import Wheel
import discord
from discord.ext import commands
from datetime import datetime

class Remote(Wheel):
    def desc(self):
        return 'fetch information through the bot remotely'

    @commands.command(
        name = 'fetchuser',
        brief = 'get a user through the bot'
    )
    async def _fetchuser(self, ctx, user: int):
        try:
            them = await self.bot.fetch_user(user)
        except discord.NotFound:
            return await ctx.send(f'user with an id of `{user}` not found')
        
        embed = ctx.make_embed(title = f'{them.name}#{them.discriminator}', description = str(them.id))
        embed.set_thumbnail(url = them.avatar_url)
        now = datetime.now()
        embed.add_field(name = 'Time spent on discord', value = f'First joined at {them.created_at}, thats over {(now - them.created_at).days} days ago')
        
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Remote(bot))
