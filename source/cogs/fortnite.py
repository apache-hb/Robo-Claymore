from discord.ext import commands
from .utils import quick_embed
import json
import sys

import aiofortnite


class Fortnite:
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('cogs/store/config.json'))
        try:
            self.client = aiofortnite.Client(
                email=self.config['fortnite']['email'],
                password=self.config['fortnite']['client'],
                launcher_token=self.config['fortnite']['launcher_token'],
                fortnite_token=self.config['fortnite']['fortnite_token'])
            self.hidden = False
        except Exception:
            print('Fortnite didnt load')
            self.hidden = True
        else:
            print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Fortnite information"
    description = "Get information about players and store sales"

    @commands.group(invoke_without_command=True)
    async def fortnite(self, ctx):
        pass

    @fortnite.command(name="playerinfo")
    async def _playerinfo(self, ctx, *, name: str):
        info = await self.client.get_user(name)
        embed = quick_embed(ctx, title='Info about {}'.format(info.username))
        embed.add_field(name='User id', value=str(info.id))
        stats = await info.stats.get()
        embed.add_field(
            name='Solo stats',
            value=
            'Score: {score}\nMatches: {matches}\nTop 12: {top12}\n Wins: {wins}\nTime:{time}\nTop 5: {top5}\nKills: {kills}'.
            format(
                score=stats['solo']['score'],
                matches=stats['solo']['matches'],
                top12=stats['solo']['top12'],
                wins=stats['solo']['wins'],
                time=stats['solo']['time'],
                top5=stats['solo']['top5'],
                kills=stats['solo']['kills']),
            inline=False)
        embed.add_field(
            name='Duo stats',
            value=
            'Score: {score}\nMatches: {matches}\nTop 12: {top12}\n Wins: {wins}\nTime:{time}\nTop 5: {top5}\nKills: {kills}'.
            format(
                score=stats['duo']['score'],
                matches=stats['duo']['matches'],
                top12=stats['duo']['top12'],
                wins=stats['duo']['wins'],
                time=stats['duo']['time'],
                top5=stats['duo']['top5'],
                kills=stats['duo']['kills']),
            inline=False)
        embed.add_field(
            name='Squad stats',
            value=
            'Score: {score}\nMatches: {matches}\nTop 12: {top12}\n Wins: {wins}\nTime:{time}\nTop 5: {top5}\nKills: {kills}'.
            format(
                score=stats['squad']['score'],
                matches=stats['squad']['matches'],
                top12=stats['squad']['top12'],
                wins=stats['squad']['wins'],
                time=stats['squad']['time'],
                top5=stats['squad']['top5'],
                kills=stats['squad']['kills']),
            inline=False)
        embed.add_field(
            name='Total stats',
            value=
            'Score: {score}\nMatches: {matches}\nTop 12: {top12}\n Wins: {wins}\nTime:{time}\nTop 5: {top5}\nKills: {kills}\nTop 3: {top3}\nTop 6: {top6}\nTop 10: {top10}\n Top 25: {top25}'.
            format(
                score=stats['all']['score'],
                matches=stats['all']['matches'],
                top12=stats['all']['top12'],
                wins=stats['all']['wins'],
                time=stats['all']['time'],
                top5=stats['all']['top5'],
                kills=stats['all']['kills'],
                top3=stats['all']['top3'],
                top6=stats['all']['top6'],
                top10=stats['all']['top10'],
                top25=stats['all']['top25']),
            inline=False)
        await ctx.send(embed=embed)

    @fortnite.command(name="news")
    async def _news(self, ctx):
        embed = quick_embed(ctx, title='Latest fortnite news')
        async for news in self.client.get_news()[:3]:
            embed.add_field(name=news.title, value=news.body, inline=False)
        await ctx.send(embed=embed)

    @fortnite.command(name="serverstatus")
    async def _serverstatus(self, ctx):
        statuses = {True: 'up', False: 'down'}
        up = await self.client.get_fortnite_status()
        await ctx.send('Fortnite servers are currently {}'.format(
            statuses[up]))

    @fortnite.command(name="leaderboard")
    async def _leaderboard(self, ctx):
        board = await self.client.get_leaderboards()
        embed = quick_embed(ctx, title='Fortnite leaderboards')
        for user in board:
            if user:
                embed.add_field(
                    name=user.name,
                    value='{}:{}'.format(user.value, user.rank),
                    inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fortnite(bot))
