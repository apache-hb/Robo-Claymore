import discord
from discord.ext import commands
from claymore import Wheel, PagedEmbed

class Owner(Wheel):
    async def cog_check(self, ctx):
        if await self.bot.is_owner(ctx.author):
            return True
        await ctx.send('Come back with a warrant')
        return False

    @commands.command(name = 'shutdown')
    async def _shutdown(self, ctx):
        await self.bot.close()

    @commands.command(name = 'test')
    async def _test(self, ctx):
        embed = PagedEmbed('test', 'something')
        for i in range(69):
            embed.add_field(name = f'name {i}', value = f'value {i}')

        await ctx.send_pages(embed)

def setup(bot):
    bot.add_cog(Owner(bot))