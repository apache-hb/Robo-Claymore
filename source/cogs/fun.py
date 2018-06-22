from discord.ext import commands
import discord
import random
import json

from .store import ball_awnsers, random_rigging, autoreact, emoji, despacito

class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        print('cog {} loaded'.format(self.__class__.__name__))

    @commands.command(name = "despacito")
    async def _despacito(self, ctx):
        for line in despacito:
            await ctx.send(line)

    @commands.command(name = "rate")
    async def _rate(self, ctx, *, thing: str):
        things = thing.lower().split(' ')
        ret = 0

        if not set(things).isdisjoint(random_rigging['bad']):
            ret = -1
        elif not set(things).isdisjoint(random_rigging['good']):
            ret = 11
        else:
            ret = random.randint(1, 10)

        await ctx.send('I rate ``{}`` a {} out of 10'.format(thing, ret))

    @commands.command(name = "coinflip")
    async def _coinflip(self, ctx, *, text: str = 'coinflip'):
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command(name = "8ball")
    async def _8ball(self, ctx, *, question: str):
        await ctx.send(random.choice(ball_awnsers))

    @commands.command(name = "compare",
    usage = 'compare <item1> and <item2>')
    async def _compare(self, ctx, *, items: str):
        ret = items.split('and')

        try:
            first = ret[0]
            second = ret[1]
        except IndexError:
            return await ctx.send('Please compare two diffrent things')

        if first.strip() in random_rigging['good']:
            awnser = 'is better than'
        elif second.strip() in random_rigging['good']:
            awnser = 'is worse than'
        elif first.strip() in random_rigging['bad']:
            awnser = 'is worse than'
        elif second.strip() in random_rigging['bad']:
            awsner = 'is better than'
        else:
            awnser = random.choice(['is better than', 'is worse than'])

        await ctx.send(first + awnser + second)

    def get_react_pair(self, phrase, react):
        return {
            'phrase': phrase,
            'react': react
        }

    @commands.group(invoke_without_command = True)
    async def autoreact(self, ctx):
        pass

    @autoreact.command(name = "add")
    async def _autoreact_add(self, ctx, *, text: str):
        text = text.split(' ')
        react = text[-1]
        phrase = ' '.join(text[:-1])

        if not emoji(react):
            return await ctx.send('you need to use an emoji as a reaction')

        for pair in autoreact:
            if pair['server_id'] == ctx.guild.id:
                for each in pair['reacts']:
                    if each['phrase'] == phrase.lower() and each['react'] == react:
                        return await ctx.send('you cannot add duplicates')

                pair['reacts'].append(self.get_react_pair(phrase.lower(), react))
                json.dump(autoreact, open('cogs/store/autoreact.json', 'w'), indent = 4)
                return await ctx.send('{} is now reacted with {}'.format(phrase, react))

    @autoreact.command(name = "remove")
    async def _autoreact_remove(self, ctx, *, phrase: str):
        for pair in autoreact:
            if pair['server_id'] == ctx.guild.id:
                for each in pair['reacts'][:]:
                    if each['phrase'] == phrase.lower():
                        pair['reacts'].remove(each)
                        json.dump(autoreact, open('cogs/store/autoreact.json', 'w'), indent = 4)
                        await ctx.send('{} is no longer reacted too'.format(phrase))

def setup(bot):
    bot.add_cog(Fun(bot))
