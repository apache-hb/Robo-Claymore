import discord
from discord.ext import commands
import random

class Polls:
    def __init__(self, bot):
        self.bot = bot
        print(f'cog {self.__class__.__name__} loaded')

    REACT_EMOTES = [
        '😂',
        '™',
        '🅱',
        '🇪',
        '🎶',
        '👌',
        '🤔',
        '😝',
        '💩',
        '🤦',
        '😉',
        '🙃',
        '😢',
        '🇧',
        '👺'
    ]

    @commands.command(name = "poll")
    @commands.cooldown(1, 100, commands.BucketType.user)
    async def _poll(self, ctx, *, choices: str):
        options: list = choices.split('or')

        if len(options) > len(self.REACT_EMOTES):
            return await ctx.send(f'the most choices possible in a poll is {len(self.REACT_EMOTES)}')

        embed = discord.Embed(title = f'{ctx.author.name}\'s poll')
        
        used_reacts: list = []

        for option in options:
            react = random.choice(self.REACT_EMOTES)

            while react in used_reacts:
                react = random.choice(self.REACT_EMOTES)

            embed.add_field(name = option, value = f'React with {react} for this option')
            used_reacts.append(react)

        msg = await ctx.send(embed = embed)

        for react in used_reacts:
            await msg.add_reaction(react)

def setup(bot):
    bot.add_cog(Polls(bot))