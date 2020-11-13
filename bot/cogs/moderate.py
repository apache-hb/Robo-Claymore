from discord.ext.commands import command
from discord import Member
from discord.ext.commands.core import has_permissions
from claymore.utils import wheel

class Moderation(wheel(desc = 'server moderation')):
    #TODO: all these
    @command()
    @has_permissions(manage_messages = True)
    async def warn(self, ctx, user: Member):
        pass

    @command()
    async def warnings(self, ctx, user: Member = None):
        pass

    @command()
    @has_permissions(administrator = True)
    async def kick(self, ctx, user: Member):
        pass

    @command()
    @has_permissions(administrator = True)
    async def ban(self, ctx, user: Member, *, reason: str = 'no reason provided'):
        pass

    @command()
    @has_permissions(manage_messages = True)
    async def mute(self, ctx, user: Member, time: str = None, *, reason: str = 'no reason provided'):
        pass

    @command()
    @has_permissions(manage_messages = True)
    async def unmute(self, ctx, user: Member):
        pass

def setup(bot):
    bot.add_cog(Moderation(bot))
