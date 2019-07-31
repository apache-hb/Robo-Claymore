from claymore import Wheel
from discord.ext import commands
import discord
from datetime import datetime

class Utils(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name = 'avatar')
    async def _avatar(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        embed = ctx.make_embed(title = 'User Avatar', description = f'Avatar for {user.name}')
        embed.set_image(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(name = 'userinfo')
    async def _userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        embed = ctx.make_embed(title = f'User info for {user.name}#{user.discriminator}', description = f'User ID: {user.id}')
        embed.set_thumbnail(url = user.avatar_url)
        embed.add_field(name = 'Is a bot', value = 'Yes' if user.bot else 'No')
        now = datetime.now()
        embed.add_field(name = f'Time spent in {ctx.guild.name}', value = f'First joined at {user.created_at}, thats over {(now - user.joined_at).days} days ago')
        embed.add_field(name = 'Time spent on discord', value = f'First joined at {user.created_at}, thats over {(now - user.created_at).days} days ago')
        embed.add_field(name = 'Roles', value = ', '.join([role.name for role in user.roles]))

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Utils(bot))