from datetime import date
from time import time
from typing import Union
from discord import Member
from discord.abc import User
from discord.ext.commands import command, guild_only
from claymore.utils import wheel, Context
from claymore.claymore import Claymore

from humanize import naturaldate, naturaldelta
from random import choice
from textwrap import dedent
from aiowolfram import Wolfram

class Utils(wheel(desc = 'helpful tools')):
    def __init__(self, bot):
        super().__init__(bot)
        wkey = bot.config['keys'].get('wolfram', None)
        if not wkey:
            self.log.warning('no api key. disabling wolfram command')
            self.wolfram.update(enabled = False)
        else:
            self.wapi = Wolfram(wkey)

    @command(
        brief = 'bot latency',
        help = """
        // get the bot to ping discord for latency
        &ping
        """
    )
    async def ping(self, ctx: Context):
        await ctx.send(f'Pong {self.bot.latency*1000:.0f}ms')

    @command(
        brief = 'randomize cases of a sentence',
        aliases = [ 'randcase', 'rcase' ],
        help = """
        // randomize the case of a sentence
        &randomcase hello world
        """
    )
    async def randomcase(self, ctx, *, text: str):
        await ctx.send(''.join(choice((str.upper, str.lower))(c) for c in text))

    @command(
        brief = 'reverse the text of a sentence',
        help = """
        // reverse a sentence
        &reverse hello world
        """
    )
    async def reverse(self, ctx, *, text: str):
        await ctx.send(text[::-1])

    @command(
        brief = 'invert the case of text',
        help = """
        // invert texts case
        &invert HELLO WORLD
        """
    )
    async def invert(self, ctx, *, text: str):
        await ctx.send(text.swapcase())

    @command(
        brief = 'bot & support invites',
        help = """
        // get an invite for the bot and for the support server
        &invite
        """
    )
    async def invite(self, ctx):
        fields = { 'invite': f'[invite me to your server](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=8)' }
        server = self.bot.config['discord'].get('invite', None)
        if server:
            fields['support'] = f'[join the support server]({server})'

        await ctx.send(embed = ctx.embed(
            'invite', 'invite me to your server', fields,
            thumbnail = self.bot.user.avatar_url
        ))

    @command(
        brief = 'user avatar',
        help = """
        // get my own avatar
        &avatar

        // get a users avatar
        &avatar @user
        """
    )
    async def avatar(self, ctx, user: User = None):
        await ctx.send((user or ctx.author).avatar_url)

    @command(
        brief = 'guild information',
        aliases = [ 'guildinfo' ],
        help = """
        // get information about the current server
        &serverinfo
        """
    )
    @guild_only()
    async def serverinfo(self, ctx):
        server = ctx.guild

        users = f"""
            ```
            {len(server.members)} total members
            {len(server.premium_subscribers)} boosting members
            ```
        """

        channels = f"""
            ```
            {len(server.text_channels)} text channels
            {len(server.voice_channels)} voice channels
            ```
        """

        def enabled(name: str):
            return '*' if name in server.features else 'x'

        features = f"""
            ```
            {enabled('VANITY_URL')}: vanity url
            {enabled('INVITE_SPLASH')}: custom invite splash
            {enabled('VERIFIED')}: verified
            {enabled('PARTNERED')}: discord partner
            {enabled('MORE_EMOJI')}: extra emote slots
            {enabled('DISCOVERABLE')}: server discovery
            {enabled('COMMUNITY')}: community server
            {enabled('COMMERCE')}: store access
            {enabled('PUBLIC')}: public server
            {enabled('NEWS')}: news channel
            {enabled('BANNER')}: custom banner
            {enabled('ANIMATED_ICON')}: animated icon
            ```
        """

        fields = {
            'users': dedent(users),
            'channels': dedent(channels),
            'emotes': f'{len(server.emojis)} custom emotes',
            'roles': f'{len(server.roles)} roles',
            'created': f'`{naturaldate(server.created_at.date())}`, {naturaldelta(date.today() - server.created_at.date())} ago',
            'owner': server.owner.mention,
            'features': (dedent(features), False)
        }

        await ctx.send(embed = ctx.embed(
            server.name, str(server.id), fields,
            thumbnail = server.icon_url
        ))

    @command(
        brief = 'user information',
        help = """
        // get information about myself
        &userinfo

        // get information about someone else
        &userinfo @user
        """
    )
    async def userinfo(self, ctx, user: Union[Member, User] = None):
        target = user or ctx.author

        then = target.created_at.date()

        fields = {
            'created': f'`{naturaldate(then)}`, {naturaldelta(date.today() - then)} ago'
        }

        if ctx.guild:
            member = ctx.guild.get_member(target.id)
            then = member.joined_at.date()
            fields['joined'] = f'`{naturaldate(then)}`, {naturaldelta(date.today() - then)} ago'

        await ctx.send(embed = ctx.embed(
            f'{target.name}#{target.discriminator}', str(target.id), fields,
            colour = target.colour,
            thumbnail = target.avatar_url
        ))

    @command(
        brief = 'user information for yourself',
        help = """
        // get information about yourself
        &selfinfo
        """
    )
    async def selfinfo(self, ctx):
        await ctx.invoke(self.userinfo)

    @command()
    async def botinfo(self, ctx):
        pass

    @command()
    async def wolfram(self, ctx, *, query: str):
        try:
            resp = await self.wapi.query(query)
        except LookupError:
            return await ctx.send(embed = ctx.embed('no results', query))

def setup(bot: Claymore):
    bot.add_cog(Utils(bot))
