from claymore import Wheel
from discord.ext import commands
import discord
from datetime import datetime
import random
from typing import Union
from utils import json
from mcstatus import MinecraftServer

POLL_EMOTES = [
    '0⃣',
    '1⃣',
    '2⃣',
    '3⃣',
    '4⃣',
    '5⃣',
    '6⃣',
    '7⃣',
    '8⃣',
    '9⃣',
    '🔟'
]

class Utils(Wheel):
    def desc(self):
        return 'utility commands'

    @commands.command(
        name = 'avatar',
        brief = 'get a users discord avatar',
        aliases = ['av']
    )
    async def _avatar(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        embed = ctx.make_embed(title = 'User Avatar', description = f'Avatar for {user.name}')
        embed.set_image(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(
        name = 'userinfo',
        brief = 'get a users info'
    )
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

    @commands.command(
        name = 'poll',
        brief = 'create a poll with multiple choices'
    )
    async def _poll(self, ctx, *, options: str):
        opts = options.split('|')

        if len(opts) not in range(len(POLL_EMOTES)):
            return await ctx.send(f'Poll must have less than {len(POLL_EMOTES)} options')

        embed = ctx.make_embed(title = f'Poll by {ctx.author.name}', description = f'{len(opts)} choices')
        for idx, opt in enumerate(opts):
            embed.add_field(name = opt, value = f'Vote with {POLL_EMOTES[idx]}')

        msg = await ctx.send(embed = embed)

        for idx in range(len(opts)):
            await msg.add_reaction(POLL_EMOTES[idx])

    @commands.command(
        name = 'selfinfo',
        brief = 'get info about yourself'
    )
    async def _selfinfo(self, ctx):
        await self._userinfo.invoke(ctx)

    @commands.command(
        name = 'ping',
        brief = 'check latency with discord api'
    )
    async def _ping(self, ctx):
        await ctx.send('Current ping to discord servers is {0:.2f}ms'.format(self.bot.latency*1000))

    @commands.command(
        name = 'serverinfo',
        brief = 'get info about the current server'
    )
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

    @commands.command(
        name = 'emoji',
        brief = 'get the url of an emote on the current server',
        aliases = ['emote']
    )
    async def _emoji(self, ctx, emoji: discord.Emoji):
        if isinstance(emoji, discord.Emoji):
            return await ctx.send(str(emoji.url))

    @commands.command(
        name = 'urban',
        brief = 'get the definition of something from the urban dictionary',
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

    @commands.command(
        name = 'mcstatus',
        brief = 'get the current status of a minecraft server'
    )
    @commands.cooldown(1, 15.0, commands.BucketType.user)
    async def _mcstatus(self, ctx, ip: str):
        try:
            server = MinecraftServer.lookup(ip)
            status = server.status()
            
            embed = ctx.make_embed(ip, status.description)
            embed.add_field(name = 'Ping', value = status.latency)
            embed.add_field(name = 'Version', value = status.version.name)
            embed.add_field(name = 'Players', value = f'{status.players.online}/{status.players.max}')
            await ctx.send(embed = embed)
        except Exception:
            await ctx.send(f'No server found at `{ip}`')

def setup(bot):
    bot.add_cog(Utils(bot))