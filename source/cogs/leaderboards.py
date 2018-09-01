import discord
from discord.ext import commands
from .utils.saved_dict import SavedDict
from .utils.shortcuts import quick_embed

class LeaderBoard:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = False
        self.user_boards = SavedDict('cogs/store/user_boards.json', '{}')
        print(f'Cog {self.__class__.__name__} loaded')

    @commands.command(name = "leaderboard")
    async def _leaderboard(self, ctx):
        pass

    @commands.command(name = "userstats")
    async def _userstats(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        embed: discord.Embed = quick_embed(ctx, title = f'stats for {user.name}')
        stats: dict = self.user_boards.data[str(user.id)]
        embed.add_field(name = 'total messages seen', value = stats['messages'])
        embed.add_field(name = 'total commands used', value = stats['commands'])
        embed.add_field(name = 'total commands broken', value = stats['errors'])
        await ctx.send(embed = embed)

    @commands.command(name = "mystats")
    async def _mystats(self, ctx):
        await ctx.invoke(self.bot.get_command('userstats'))

    async def on_message(self, ctx):
        try:
            self.user_boards.data[str(ctx.author.id)]
        except KeyError:
            self.user_boards.data[str(ctx.author.id)] = {
                'messages': 0, #total messages visible to the bot
                'commands': 0, #total commands invoked
                'errors': 0 #amount of times they've broken a command
            }
        self.user_boards.data[str(ctx.author.id)]['messages'] += 1
        self.user_boards.save()

    async def on_command(self, ctx):
        self.user_boards.data[str(ctx.author.id)]['commands'] += 1
        self.user_boards.save()

    async def on_command_error(self, ctx, err):
        self.user_boards.data[str(ctx.author.id)]['errors'] += 1
        self.user_boards.save()

def setup(bot):
    bot.add_cog(LeaderBoard(bot))
