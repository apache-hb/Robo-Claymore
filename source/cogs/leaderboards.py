import discord
from discord.ext import commands
from .utils.saved_dict import SavedDict

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
    async def _userstats(self, ctx, user: discord.User):
        pass

    @commands.command(name = "mystats")
    async def _mystats(self, ctx):
        pass

    async def on_message(self, ctx):
        try:
            self.user_boards.data[str(ctx.author.id)]
        except KeyError:
            self.user_boards.data[str(ctx.author.id)] = {
                'messages': 0, #total messages visible to the bot
                'commands': 0, #total commands invoked
                'errors': 0, #amount of times they've broken a command
                'exp': 0, #experience
                'count': 0 #how many times they've counted
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
