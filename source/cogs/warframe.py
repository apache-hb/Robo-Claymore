from discord.ext import commands

from .store import frames
from .utils import quick_embed

import time
import json
import aiohttp


class Warframe:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))

    short = "Warframe info"
    description = "Get info about an item or event in warframe"

    @commands.group(invoke_without_command=True)
    async def warframe(self, ctx):
        embed = quick_embed(ctx, title='All warframe subcommands')
        for a in self.warframe.walk_commands():
            embed.add_field(name=a.name, value=a.brief)
        await ctx.send(embed=embed)

    @warframe.command(name="weaponinfo", brief="Get info about a weapon")
    async def _weaponinfo(self, ctx, *, item: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://api.warframestat.us/weapons/search/{query}'.
                    format(query=item.lower())) as resp:
                ret = json.loads(await resp.text())
                if not ret:
                    return await ctx.send(
                        'Nothing with the name {} found'.format(item))

                embed = quick_embed(ctx, title='Info about {}'.format(item))
                for weapon in ret:
                    a.append(f['name'])
                if weapon:
                    embed.add_field(name='Variants', value=', '.join(a))
                embed.add_field(name='Name', value=ret[0]['name'])
                embed.add_field(name='More info', value=ret[0]['url'])
                embed.add_field(name='Minimum MR rank', value=ret[0]['mr'])
                embed.add_field(name='Type', value=ret[0]['type'])

                try:
                    embed.add_field(
                        name='Base damage',
                        value=
                        'Total of {full}, comprised of {pun} Puncture, {imp} Impact and {sla} Slash'.
                        format(
                            full=ret[0]['damage'],
                            pun=ret[0]['puncture'],
                            imp=ret[0]['impact'],
                            sla=ret[0]['slash']))
                except KeyError:
                    embed.add_field(name='Base damage', value=j[0]['damage'])

                if j[0]['type'] == 'Melee':
                    if j[0]['polarities']:
                        embed.add_field(
                            name='Default polarities',
                            value=', '.join(j[0]['polarities']))
                    embed.add_field(name='Attack speed', value=ret[0]['speed'])
                    embed.add_field(name='Slide damage', value=ret[0]['slide'])
                    embed.add_field(
                        name='Slam attack damage', value=ret[0]['jump'])
                    embed.add_field(
                        name='Wall attack damage', value=ret[0]['wall'])
                    embed.add_field(
                        name='Channeling efficiency', value=ret[0]['channeling'])
                    embed.add_field(
                        name='Default stance polarity',
                        value=ret[0]['stancePolarity'])
                elif ret[0]['type'] in ['Primary', 'Secondary']:

                    try:
                        embed.add_field(
                            name='Noise level', value=ret[0]['noise'])
                    except KeyError:
                        pass

                    try:
                        embed.add_field(name='Firerate', value=ret[0]['speed'])
                    except KeyError:
                        pass

                    try:
                        embed.add_field(
                            name='Accuracy', value=ret[0]['accuracy'])
                    except KeyError:
                        pass

                    try:
                        embed.add_field(
                            name='Maximum ammo capacity', value=ret[0]['ammo'])
                    except KeyError:
                        pass

                    embed.add_field(
                        name='Magazine capacity', value=ret[0]['magazine'])
                    embed.add_field(name='Reload speed', value=ret[0]['reload'])
                    embed.add_field(
                        name='Projectile type', value=ret[0]['projectile'])
                    embed.add_field(name='Trigger type', value=ret[0]['trigger'])

                    try:
                        embed.add_field(
                            name='Flight speed', value=ret[0]['flight'])
                    except KeyError:
                        pass

                embed.add_field(
                    name='Critical chance', value=ret[0]['crit_chance'])
                embed.add_field(
                    name='Critical damage multiplier', value=ret[0]['crit_mult'])
                embed.add_field(
                    name='Status chance', value=ret[0]['status_chance'])
                embed.add_field(
                    name='Riven disposition', value=ret[0]['riven_disposition'])
                embed.set_thumbnail(url=ret[0]['thumbnail'])

                return await ctx.send(embed=embed)

    @warframe.command(
        name="dropinfo",
        brief="Get info about the drop rates and location of an item")
    async def _dropinfo(self, ctx, *, item: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://api.warframestat.us/drops/search/{query}'.format(
                        query=item.lower())) as resp:
                ret = json.loads(await resp.text())
                if not j:
                    return await ctx.send(
                        'Nothing with the name {item} found'.format(item=item))

                embed = quick_embed(
                    ctx, title='Information about {}'.format(item))

                count = -1
                for location in ret:
                    count += 1
                    if a < 25:
                        embed.add_field(
                            name='Item {} drops from {}'.format(
                                location['item'], location['place']),
                            value='Rarity of {} & a drop chance of {}%'.format(
                                location['rarity'], location['chance']))
                    else:
                        break

                await ctx.send(embed=embed)

    def polarity_converter(self, polarities):
        return polarities.replace(
                        '<:madurai:319586146499690496>', 'Maduri').replace(
                            '<:naramon:319586146478850048>',
                            'Naramon').replace('<:vazarin:319586146269003778>',
                                               'Varazin'))

    @warframe.command(
        name="frameinfo", brief="Get info and stats about a certain frame")
    async def _frameinfo(self, ctx, *, target: str):
        for frame in frames:
            if target.lower() in frame['regex']:
                try:
                    color = frame['color']
                except KeyError:
                    color = ctx.guild.me.color

                embed = quick_embed(
                    ctx,
                    title='Info about {}'.format(frame['name']),
                    description=frame['url'],
                    colour=color)
                embed.add_field(name='Min/Max Health', value=frame['health'])
                embed.add_field(name='Min/Max Shields', value=frame['shield'])
                embed.add_field(name='Base armor', value=frame['armor'])
                embed.add_field(name='Min/Max power', value=frame['power'])
                embed.add_field(name='Base speed', value=frame['speed'])

                try:
                    embed.add_field(name='More info', value=frame['info'])
                except KeyError:
                    pass

                if not frame['aura'] == '':
                    embed.add_field(
                        name='Default aura polarity',
                        value=self.polarity_converter(frame['aura'])
                embed.add_field(
                    name='Default polarities',
                    value=self.polarity_converter(', '.join(frame['polarities']))

                try:
                    embed.add_field(
                        name='In game description', value=frame['description'])
                except KeyError:
                    pass

                try:
                    embed.add_field(
                        name='Main drop location', value=frame['location'])
                except KeyError:
                    pass

                try:
                    embed.set_thumbnail(url=frame['thumbnail'])
                except KeyError:
                    pass

                await ctx.send(embed=embed)

    @warframe.command(name="sortie", brief="todays sortie")
    async def _sortie(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://api.warframestat.us/pc/sortie') as resp:
                ret = json.loads(await resp.text())
                embed = quick_embed(ctx, title='Todays sorties')
                count = 0
                for mission in ret['variants']:
                    count += 1
                    embed.add_field(
                        name='Mission {}'.format(b),
                        value=
                        'Mission type: {mission}, Modifier: {mod}, Location: {loc}'.
                        format(
                            mission=mission['missionType'],
                            mod=mission['modifier'],
                            loc=mission['node']),
                        inline=False)
                embed.set_footer(text='Sortie for {}'.format(time.time()))
                await ctx.send(embed=embed)

    @warframe.command(name="alerts", brief="ongoing alerts")
    async def _alerts(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://api.warframestat.us/pc/alerts') as resp:
                ret = json.loads(await resp.text())
                embed = quick_embed(ctx, title='Currently running alerts')
                count = 0
                for alert in ret:
                    count += 1
                    embed.add_field(
                        name='Alert {}'.format(count),
                        value=
                        'Location: {loc}, Mission type: {mis}, Faction: {fac}'.
                        format(
                            loc=alert['mission']['node'],
                            mis=alert['mission']['type'],
                            fac=alert['mission']['faction']))
                    embed.add_field(
                        name='Information',
                        value='Rewards: {reward}, Expires in: {exp}'.format(
                            reward=alert['mission']['reward']['asString'],
                            exp=alert['eta']))
                await ctx.send(embed=embed)

    @warframe.command(name="baro", brief="Baro Ki\'Teer, void trader")
    async def _baro(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://api.warframestat.us/pc/voidTrader') as resp:
                ret = json.loads(await resp.text())
                embed = quick_embed(ctx, title='Current Baro Ki\'Teer info')
                if not ret['active']:
                    embed.add_field(
                        name='BaroKi\'teer',
                        value=
                        'Is currently not visiting, he will be back in {}'.
                        format(ret['startString']))
                    return await ctx.send(embed=embed)
                embed.add_field(name='Location', value=ret['location'])
                embed.add_field(
                    name='Current inventory', value=', '.join(ret['inventory']))
                await ctx.send(embed=embed)

    @warframe.command(name="darvo", brief="Todays darvo deal")
    async def _darvo(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://api.warframestat.us/pc/dailyDeals') as resp:
                ret = json.loads(await resp.text())
                embed = quick_embed(
                    ctx,
                    title='Current Darvo Deal',
                    description=
                    'Could i interest you in some half price life support?')
                embed.add_field(name='Item', value=ret[0]['item'])
                embed.add_field(
                    name='Discount',
                    value=
                    'Original price: {org}, Percentage discount: {dis}%, Current price: {cur}'.
                    format(
                        org=ret[0]['originalPrice'],
                        dis=ret[0]['discount'],
                        cur=ret[0]['salePrice']))
                embed.add_field(name='Amount sold', value=str(ret[0]['sold']))
                embed.add_field(name='Time left', value=ret[0]['eta'])
                await ctx.send(embed=embed)

    @warframe.command(name="cetustime", brief="current time in the plains")
    async def _cetustime(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://api.warframestat.us/pc/cetusCycle') as resp:
                j = json.loads(await resp.text())
                embed = quick_embed(
                    ctx,
                    title='Current cetus time',
                    description=
                    'Taken from https://api.warframestat.us/pc/cetusCycle')
                embed.add_field(name='Time', value=j['isDay'])
                embed.add_field(name='Cycle ID', value=j['id'])
                embed.add_field(name='Time left', value=j['timeLeft'])
                embed.add_field(name='Quick info', value=j['shortString'])
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Warframe(bot))
