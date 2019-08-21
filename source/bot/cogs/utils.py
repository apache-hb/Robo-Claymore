from claymore import Wheel
from discord.ext import commands
import discord
from datetime import datetime
import random
from typing import Union
from utils import json

class Utils(Wheel):
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
        embed.add_field(name = 'Time spent on discord', value = f'First joined at {user.created_at}, thats over {(now - user.created_at).days} days ago')

        if ctx.guild is not None:
            embed.add_field(name = f'Time spent in {ctx.guild.name}', value = f'First joined at {user.created_at}, thats over {(now - user.joined_at).days} days ago')
            embed.add_field(name = 'Roles', value = ', '.join([role.name for role in user.roles]))

        await ctx.send(embed = embed)

    @commands.command(name = 'selfinfo')
    async def _selfinfo(self, ctx):
        await self._userinfo.invoke(ctx)

    @commands.command(name = 'ping')
    async def _ping(self, ctx):
        await ctx.send(f'Current ping to discord servers is {round(self.bot.latency()/1000)}ms')

    @commands.command(name = 'serverinfo')
    @commands.guild_only()
    async def _serverinfo(self, ctx):
        embed = ctx.make_embed('Server info', f'for server {ctx.guild.name}')
        embed.add_field(name = 'Owner', value = ctx.guild.owner.mention)
        embed.add_field(name = 'Region', value = ctx.guild.region)
        embed.add_field(name = 'Total members', value = len(ctx.guild.members))
        embed.add_field(name = 'Text channels', value = len(ctx.guild.text_channels))
        embed.add_field(name = 'Voice channels', value = len(ctx.guild.voice_channels))
        now = datetime.now()
        then = ctx.guild.created_at
        embed.add_field(name = 'Age', value = f'Created at `{then.strftime("%Y-%m-%d")}`, thats over {str(now - then)} ago')
        embed.add_field(name = 'Roles', value = ', '.join([role.name for role in ctx.guild.roles]))
        embed.set_footer(text = f'Server ID: {ctx.guild.id}')
        embed.set_thumbnail(url = ctx.guild.icon_url)

        await ctx.send(embed = embed)

    @commands.command(name = 'avatar')
    async def _avatar(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author

        await ctx.send(user.avatar_url)

    @commands.command(name = 'emoji')
    async def _emoji(self, ctx, emoji: discord.Emoji):
        if isinstance(emoji, discord.Emoji):
            return await ctx.send(str(emoji.url))

    @commands.command(
        name = 'urban',
        aliases = [ 'urbandict' ]
    )
    async def _urban(self, ctx, *, query: str = None):
        if query is None:
            url = 'http://api.urbandictionary.com/v0/random'
        else:
            url = f'http://api.urbandictionary.com/v0/define?term={query}'

        data = await json(url)

        if not data['list']:
            return await ctx.send(embed = ctx.make_embed(f'Search for {query} was blank'))

        post = random.choice(data['list'])

        embed = ctx.make_embed(f'Definition of {post["word"]}', description = f'Written by {post["author"]}')
        embed.add_field(name = 'Definition', value = post['definition'])
        embed.add_field(name = 'Example', value = post['example'])
        embed.add_field(name = 'Link', value = post['permalink'])
        embed.set_footer(text = f'Rating {post["thumbs_up"]}/{post["thumbs_down"]}')

        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Utils(bot))