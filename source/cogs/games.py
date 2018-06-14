from discord.ext import commands
import discord
from .store import quick_embed, titanfall_pilot_variables
import aiohttp
import time
import json
import random

class Games:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        self.frames = None#used for warframe cache
        print('cog {} loaded'.format(self.__class__.__name__))

    @classmethod
    def polarity_converter(self, text: str):
        return text.replace('<:madurai:319586146499690496>', 'Maduri').replace('<:naramon:319586146478850048>', 'Naramon').replace('<:vazarin:319586146269003778>', 'Varazin')

    @commands.group(invoke_without_command = True)
    async def warframe(self, ctx):
        embed = quick_embed(ctx, title = 'All the subcommands for warframe')
        b = []
        for a in self.warframe.walk_commands():
            if a.name not in b:
                embed.add_field(name = a.name, value = a.brief)
            b.append(a.name)
        await ctx.send(embed = embed)

    @warframe.command(name = "weaponinfo")
    async def _warframe_weaponinfo(self, ctx, *, name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/weapons/search/{}'.format(name.lower())) as resp:
                ret = json.loads(await resp.text())

                if not ret:
                    return await ctx.send('{} was not found in the warframe database'.format(name))

                embed = quick_embed(ctx, title = 'Information about {}'.format(name), description = 'Taken from the official warframe database')

                a = []
                for weapon in ret:
                    a.append(weapon['name'])
                if a:
                    embed.add_field(name = 'Variants', value = ', '.join(a))
                embed.add_field(name = 'Name', value = ret[0]['name'])
                embed.add_field(name = 'More info', value = ret[0]['url'])
                embed.add_field(name = 'Minimum mastery rank', value = ret[0]['mr'])
                embed.add_field(name = 'Type', value = ret[0]['type'])

                try:
                    embed.add_field(name = 'Base damage',
                    value = 'A total of {} damage comprised of {} slash, {} puncture and {} impact'.format(
                        ret[0]['damage'],
                        ret[0]['slash'],
                        ret[0]['puncture'],
                        ret[0]['impact']
                    ))
                except KeyError:
                    embed.add_field(name = 'Base damage', value = ret[0]['damage'])

                if ret[0]['type'] == 'Melee':
                    if ret[0]['polarities']:
                        embed.add_field(name = 'Default polarities', value = ', '.join(ret[0]['polarities']))
                        embed.add_field(name = 'Attack speed', value = ret[0]['speed'])
                        embed.add_field(name = 'Slide attack damage', value = ret[0]['slide'])
                        embed.add_field(name = 'Slam attack damage', value = ret[0]['jump'])
                        embed.add_field(name = 'Wall attack damage', value = ret[0]['wall'])
                        embed.add_field(name = 'Channeling efficiency', value = ret[0]['channeling'])
                        embed.add_field(name = 'Default stance polarity', value = ret[0]['stancePolarity'])

                elif ret[0]['type'] in ['Primary', 'Secondary']:
                    try: embed.add_field(name='Noise level', value=ret[0]['noise'])
                    except KeyError: pass

                    try: embed.add_field(name='Firerate', value=ret[0]['speed'])
                    except KeyError: pass

                    try: embed.add_field(name='Accuracy', value=ret[0]['accuracy'])
                    except KeyError:pass

                    try: embed.add_field(name='Maximum ammo capacity', value=ret[0]['ammo'])
                    except KeyError: pass

                    embed.add_field(name='Magazine capacity', value=ret[0]['magazine'])
                    embed.add_field(name='Reload speed', value=ret[0]['reload'])
                    embed.add_field(name='Projectile type', value=ret[0]['projectile'])
                    embed.add_field(name='Trigger type', value=ret[0]['trigger'])

                    try: embed.add_field(name='Flight speed', value=ret[0]['flight'])
                    except KeyError:pass

                embed.add_field(name = 'Critical chance', value = ret[0]['crit_chance'])
                embed.add_field(name = 'Critical damage multiplier', value = ret[0]['crit_mult'])
                embed.add_field(name = 'Status chance', value = ret[0]['status_chance'])
                embed.add_field(name = 'Riven disposition', value = ret[0]['riven_disposition'])
                embed.set_thumbnail(url = ret[0]['thumbnail'])

                await ctx.send(embed = embed)

    @warframe.command(name = "dropinfo")
    async def _warframe_dropinfo(self, ctx, *, name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/drops/search/{}'.format(name.lower())) as resp:
                ret = json.loads(await resp.text())

                if not ret:
                    return await ctx.send('{} was not found in the warframe database'.format(name))

                embed = quick_embed(ctx, title = 'Information about {}'.format(name), description = 'Taken from the warframe database')

                for location in ret[:25]:
                    embed.add_field(name = 'Item {} drops from {}'.format(location['item'], location['place']),
                    value = 'Rarity of {}% & a drop chance of {}%'.format(location['rarity'], location['chance']))

                await ctx.send(embed = embed)

    @warframe.command(name = "frameinfo")
    async def _warframe_frameinfo(self, ctx, *, name: str):
        if self.frames is None:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.warframestat.us/warframes') as resp:
                    self.frames = json.loads(await resp.text())

        for frame in self.frames:
            if name.lower() in frame['regex']:

                try: colour = frame['color']
                except KeyError: colour = 0x023cfc

                embed = quick_embed(ctx, title = frame['name'], description = frame['url'], colour = colour)

                embed.add_field(name = 'min/max health', value = frame['health'])
                embed.add_field(name = 'min/max shields', value = frame['shield'])
                embed.add_field(name = 'Base armor', value = frame['armor'])
                embed.add_field(name = 'min/max power', value = frame['power'])
                embed.add_field(name = 'sprint speed', value = frame['speed'])

                try: embed.add_field(name = 'More info', value = frame['info'])
                except KeyError: pass

                if not frame['aura'] == '':
                    embed.add_field(name = 'Default aura polarity', value = self.polarity_converter(frame['aura']))

                embed.add_field(name = 'Default polarities', value = self.polarity_converter(', '.join(frame['polarities'])))

                try: embed.add_field(name = 'In game description', value = frame['description'])
                except KeyError: pass

                try: embed.add_field(name = 'Main drop location', value = frame['location'])
                except KeyError: pass

                try: embed.set_thumbnail(url = frame['thumbnail'])
                except KeyError: pass

                return await ctx.send(embed = embed)

        await ctx.send('No frame called {} found'.format(name))

    @warframe.command(name = "sortie")
    async def _warframe_sortie(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/sortie') as resp:
                ret = json.loads(await resp.text())

                embed = quick_embed(ctx, title = 'Todays sortie', description = 'From the official warframe database')

                for index, value in enumerate(ret['variants'], start = 1):

                    embed.add_field(name = 'Mission {}'.format(index),
                    value = 'Mission type: {}\nModifier: {}\nLocation: {}'.format(
                        value['missionType'],
                        value['modifier'],
                        value['node']
                    ), inline = False)

                embed.set_footer(text = 'Sortie for {}'.format(time.time()))

                return await ctx.send(embed = embed)

    @warframe.command(name = "alert")
    async def _warframe_alert(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/alerts') as resp:

                ret = json.loads(await resp.text())

                embed = quick_embed(ctx, title = 'Currently running sorties', description = 'Taken from the warframe web api')

                for index, alert in enumerate(ret):
                    embed.add_field(name = 'Alert {}'.format(index),
                    value = 'Location {}\nMission type: {}\nFaction: {}\nRewards: {}\nExpires in: {}'.format(
                        alert['mission']['node'],
                        alert['mission']['type'],
                        alert['mission']['faction'],
                        alert['mission']['reward']['asString'],
                        alert['eta']
                    ), inline = False)

                await ctx.send(embed = embed)

    @warframe.command(name = "baro")
    async def _warframe_baro(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/voidTrader') as resp:

                ret = json.loads(await resp.text())

                embed = quick_embed(ctx, title = 'BaroKi\'teer')

                if not ret['active']:
                    embed.add_field(name = 'Is currently away in the void',
                    value = 'He will be back in {}'.format(ret['startString']))

                    return await ctx.send(embed = embed)

                embed.add_field(name = 'Location', value = ret['location'])
                embed.add_field(name = 'Current inventory', value = ', '.join(ret['inventory']))

                await ctx.send(embed = embed)

    @warframe.command(name = "darvo")
    async def _warframe_darvo(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/dailyDeals') as resp:

                ret = json.loads(await resp.text())

                embed = quick_embed(ctx, title = 'Current Darvo deal',
                description = 'Could I interest you in some half price life support')

                embed.add_field(name = 'Item', value = ret[0]['item'])
                embed.add_field(name = 'Discount',
                vlaue = 'Original price: {}\nPercentage discount: {}\nCurrent price: {}'.format(
                    ret[0]['originalPrice'],
                    ret[0]['discount'],
                    ret[0]['salePrice']
                ))

                embed.add_field(name = 'Amount sold', value = str(ret[0]['sold']))
                embed.add_field(name = 'Time left', value = ret[0]['eta'])

                await ctx.send(embed = embed)

    @warframe.command(name = "cetustime")
    async def _warframe_cetustime(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/cetusCycle') as resp:

                ret = json.loads(await resp.text())

                embed = quick_embed(ctx, title = 'Current time on cetus',
                description = 'Taken from the warframe web api')

                embed.add_field(name = 'Time', value = ret['isDay'])
                embed.add_field(name = 'Cycle ID', value = ret['id'])
                embed.add_field(name = 'Time left', value = ret['timeLeft'])
                embed.add_field(name = 'Quick info', value = ret['shortString'])

                await ctx.send(embed = embed)

    @commands.group(invoke_without_command = True)
    async def titanfall(self, ctx):
        embed = quick_embed(ctx, title = 'All the subcommands for titanfall')
        b = []
        for a in self.titanfall.walk_commands():
            if a.name not in b:
                embed.add_field(name = a.name, value = a.brief)
            b.append(a.name)
        await ctx.send(embed = embed)

    @titanfall.command(name = "randompilot")
    async def _titanfall_randompilot(self, ctx):
        ret = '{} Here is a random loadout```diff\n'.format(ctx.author.mention)

        ret += '+ Pilot: ' + random.choice(titanfall_pilot_variables['pilots']) + '\n'
        ret += '- Grenade: ' + random.choice(titanfall_pilot_variables['grenades']) + '\n'
        ret += '+ Primary: ' + random.choice(titanfall_pilot_variables['primary']) + '\n'
        ret += '- Secondary: ' + random.choice(titanfall_pilot_variables['secondary']) + '\n'
        ret += '+ Anti Titan: ' + random.choice(titanfall_pilot_variables['anti_titan']) + '\n'
        ret += '- First Perk: ' + random.choice(titanfall_pilot_variables['perk_slot_a']) + '\n'
        ret += '+ Second Perk: ' + random.choice(titanfall_pilot_variables['perk_slot_b']) + '\n'
        ret += '\n```'
        await ctx.send(ret)

    @titanfall.command(name = "randomtitan", brief = "soon™")
    async def _titanfall_randomtitan(self, ctx):
        await ctx.send('soon™')

    @titanfall.command(name = "randomloadout", brief = "soon™")
    async def _titanfall_randomloadout(self, ctx):
        await ctx.send('soon™')

def setup(bot):
    bot.add_cog(Games(bot))