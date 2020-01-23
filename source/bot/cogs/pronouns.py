import discord
from discord.ext import commands
from claymore import Wheel

class Pronouns(Wheel):
    def desc(self):
        return 'Set pronouns for a user'

    @commands.command(
        name = 'addpronoun',
        brief = 'add pronouns to the current server for users to use'
    )
    @commands.guild_only()
    async def _addpronoun(self, ctx, name: str):
        pass

    @commands.command(
        name = 'givepronoun',
        brief = 'give a user a pronoun'
    )
    @commands.guild_only()
    async def _givepronoun(self, ctx, user: discord.Member, pronoun: str):
        pass

    @commands.command(
        name = 'removepronoun',
        brief = 'remove a pronoun from a user'
    )
    @commands.guild_only()
    async def _removepronoun(self, ctx, user: discord.Member, pronoun: str):
        pass

    @commands.command(
        name = 'deletepronoun',
        brief = 'delete a pronoun from the server'
    )
    @commands.guild_only()
    async def _deletepronoun(self, ctx, pronoun: str):
        pass

def setup(bot):
    bot.add_cog(Pronouns(bot))