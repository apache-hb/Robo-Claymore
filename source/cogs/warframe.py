import discord
from discord.ext import commands

from .store import style_embed, pyout, Store

import sys

import time
import json
import aiohttp

class Warframe:
    def __init__(self, bot):
        self.bot = bot
        pyout('Cog {} loaded'.format(self.__class__.__name__))

    short = "Warframe info"
    description = "Get info about an item or event in warframe"

    @commands.group(invoke_without_command=True)
    async def warframe(self, ctx):
        embed=style_embed(ctx, title='All warframe subcommands')
        for a in self.warframe.walk_commands():
            try:
                embed.add_field(name=a.name, value=a.brief)
            except AttributeError:
                embed.add_field(name=a.name, value='Subcommand of Warframe')
        await ctx.send(embed=embed)

    @warframe.command(name="weaponinfo")
    async def _weaponinfo(self, ctx, *, item: str):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/weapons/search/{query}'.format(query=item.lower())) as resp:
                j = json.loads(await resp.text())
                if not j:
                    return await ctx.send('Nothing with the name {} found'.format(item))

                embed=style_embed(ctx, title='Info about {}'.format(item))
                a = []
                for f in j:
                    a.append(f['name'])
                if f:
                    embed.add_field(name='Variants', value=', '.join(a))
                embed.add_field(name='Name', value=j[0]['name'])
                embed.add_field(name='More info', value=j[0]['url'])
                embed.add_field(name='Minimum MR rank', value=j[0]['mr'])
                embed.add_field(name='Type', value=j[0]['type'])
                    
                try:
                    embed.add_field(name='Base damage', 
                    value='Total of {full}, comprised of {pun} Puncture, {imp} Impact and {sla} Slash'.format(
                        full=j[0]['damage'],
                        pun=j[0]['puncture'],
                        imp=j[0]['impact'],
                        sla=j[0]['slash']))
                except KeyError:
                    embed.add_field(name='Base damage',
                    value=j[0]['damage'])
                    
                if j[0]['type'] == 'Melee':
                    if j[0]['polarities']:
                        embed.add_field(name='Default polarities', value=', '.join(j[0]['polarities']))
                    embed.add_field(name='Attack speed', value=j[0]['speed'])
                    embed.add_field(name='Slide damage', value=j[0]['slide'])
                    embed.add_field(name='Slam attack damage', value=j[0]['jump'])
                    embed.add_field(name='Wall attack damage', value=j[0]['wall'])
                    embed.add_field(name='Channeling efficiency', value=j[0]['channeling'])
                    embed.add_field(name='Default stance polarity', value=j[0]['stancePolarity'])
                elif j[0]['type'] in ['Primary', 'Secondary']:

                    try: embed.add_field(name='Noise level', value=j[0]['noise'])
                    except KeyError: pass
                        
                    try: embed.add_field(name='Firerate', value=j[0]['speed'])
                    except KeyError: pass
                        
                    try: embed.add_field(name='Accuracy', value=j[0]['accuracy'])
                    except KeyError: pass

                    try: embed.add_field(name='Maximum ammo capacity', value=j[0]['ammo'])
                    except KeyError: pass

                    embed.add_field(name='Magazine capacity', value=j[0]['magazine'])
                    embed.add_field(name='Reload speed', value=j[0]['reload'])
                    embed.add_field(name='Projectile type', value=j[0]['projectile'])
                    embed.add_field(name='Trigger type', value=j[0]['trigger'])
                
                    try: embed.add_field(name='Flight speed', value=j[0]['flight'])
                    except KeyError: pass
                    
                embed.add_field(name='Critical chance', value=j[0]['crit_chance'])
                embed.add_field(name='Critical damage multiplier', value=j[0]['crit_mult'])
                embed.add_field(name='Status chance', value=j[0]['status_chance'])
                embed.add_field(name='Riven disposition', value=j[0]['riven_disposition'])
                embed.set_thumbnail(url=j[0]['thumbnail'])
                return await ctx.send(embed=embed)

    @warframe.command(name="dropinfo")
    async def _dropinfo(self, ctx, *, item: str):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/drops/search/{query}'.format(query=item.lower())) as resp:
                j = json.loads(await resp.text())
                if not j:
                    return await ctx.send('Nothing with the name {item} found'.format(item=item))
                    
                embed=style_embed(ctx, title='Information about {}'.format(item))

                a=-1
                for loc in j:
                    a+=1
                    if a < 25:
                        embed.add_field(name='Item {} drops from {}'.format(loc['item'], loc['place']), 
                        value='Rarity of {} & a drop chance of {}%'.format(loc['rarity'], loc['chance']))
                    else:
                        break
                
                await ctx.send(embed=embed)

    @warframe.command(name="frameinfo")
    async def _frameinfo(self, ctx, *, target: str):
        for frame in Store.frames:
            if target.lower() in frame['regex']:
                try:
                    color = frame['color']
                except KeyError:
                    color = ctx.guild.me.color
                
                embed=style_embed(ctx, title='Info about {}'.format(frame['name']),
                description=frame['url'], 
                color=color)
                embed.add_field(name='Min/Max Health', value=frame['health'])
                embed.add_field(name='Min/Max Shields', value=frame['shield'])
                embed.add_field(name='Base armor', value=frame['armor'])
                embed.add_field(name='Min/Max power', value=frame['power'])
                embed.add_field(name='Base speed', value=frame['speed'])
                
                try: embed.add_field(name='More info', value=frame['info'])
                except KeyError: pass

                if not frame['aura'] =='':
                    embed.add_field(name='Default aura polarity', 
                    value=frame['aura'].replace('<:madurai:319586146499690496>', 
                    'Maduri').replace('<:naramon:319586146478850048>', 
                    'Naramon').replace('<:vazarin:319586146269003778>', 'Varazin'))
                embed.add_field(name='Default polarities',
                value=', '.join(frame['polarities']).replace('<:madurai:319586146499690496>', 
                'Maduri').replace('<:naramon:319586146478850048>', 
                'Naramon').replace('<:vazarin:319586146269003778>', 'Varazin'))

                try: embed.add_field(name='In game description', value=frame['description'])
                except KeyError: pass

                try: embed.add_field(name='Main drop location', value=frame['location'])
                except KeyError: pass

                try: embed.set_thumbnail(url=frame['thumbnail'])
                except KeyError: pass

                await ctx.send(embed=embed)

    @warframe.command(name="sortie")
    async def _sortie(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/sortie') as resp:
                j = json.loads(await resp.text())
                embed = style_embed(ctx, title='Todays sorties')
                b=0
                for a in j['variants']:
                    b+=1
                    embed.add_field(name='Mission {}'.format(b), 
                    value='Mission type: {mission}, Modifier: {mod}, Location: {loc}'.format(
                        mission=a['missionType'],
                        mod=a['modifier'],
                        loc=a['node']
                    ), inline=False)
                embed.set_footer(text='Sortie for {}'.format(time.time()))
                await ctx.send(embed=embed)

    @warframe.command(name="alerts")
    async def _alerts(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/alerts') as resp:
                j = json.loads(await resp.text())
                embed = style_embed(ctx, title='Currently running alerts')
                b=0
                for a in j:
                    b+=1
                    embed.add_field(name='Alert {}'.format(b),
                    value='Location: {loc}, Mission type: {mis}, Faction: {fac}'.format(
                        loc=a['mission']['node'],
                        mis=a['mission']['type'],
                        fac=a['mission']['faction']
                    ))
                    embed.add_field(name='Information', 
                    value='Rewards: {reward}, Expires in: {exp}'.format(
                        reward=a['mission']['reward']['asString'],
                        exp=a['eta']
                    ))
                await ctx.send(embed=embed)
                
    @warframe.command(name="baro")
    async def _baro(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/voidTrader') as resp:
                j = json.loads(await resp.text())
                embed = style_embed(ctx, title='Current Baro Ki\'Teer info')
                if not j['active']:
                    embed.add_field(name='BaroKi\'teer', value='Is currently not visiting, he will be back in {}'.format(
                        j['startString']
                    ))
                    return await ctx.send(embed=embed)
                embed.add_field(name='Location', value=j['location'])
                embed.add_field(name='Current inventory', value=', '.join(j['inventory']))
                await ctx.send(embed=embed)

    @warframe.command(name="darvo")
    async def _darvo(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/dailyDeals') as resp:
                j = json.loads(await resp.text())
                embed = style_embed(ctx, title='Current Darvo Deal', 
                description='Could i interest you in some half price life support?')
                embed.add_field(name='Item', value=j[0]['item'])
                embed.add_field(name='Discount', 
                value='Original price: {org}, Percentage discount: {dis}%, Current price: {cur}'.format(
                    org=j[0]['originalPrice'],
                    dis=j[0]['discount'],
                    cur=j[0]['salePrice']
                ))
                embed.add_field(name='Amount sold',
                value=str(j[0]['sold']))
                embed.add_field(name='Time left', value=j[0]['eta'])
                await ctx.send(embed=embed)

    @warframe.command(name="cetustime")
    async def _cetustime(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.warframestat.us/pc/cetusCycle') as resp:
                j = json.loads(await resp.text())
                embed=style_embed(ctx, title='Current cetus time', 
                description='Taken from https://api.warframestat.us/pc/cetusCycle')
                embed.add_field(name='Time', value=j['isDay'])
                embed.add_field(name='Cycle ID', value=j['id'])
                embed.add_field(name='Time left', value=j['timeLeft'])
                embed.add_field(name='Quick info', value=j['shortString'])
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Warframe(bot))