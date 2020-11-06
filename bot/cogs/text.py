from typing import Union
from discord.ext.commands.core import group, guild_only, has_permissions
from discord import Emoji
from claymore.utils import wheel
from discord.ext.commands import command

class Text(wheel(desc = 'automatic messages')):
    @group()
    async def reacts(self, ctx):
        pass

    @reacts.command()
    async def add(self, ctx, emote: Emoji, *, text: str):
        pass

    @reacts.command()
    async def remove(self, ctx, *, it: Union[Emoji, str]):
        pass

    @group()
    async def welcome(self, ctx, *, msg: str):
        pass

    @welcome.command()
    async def enable(self, ctx):
        pass

    @welcome.command()
    async def disable(self, ctx):
        pass

    @group()
    async def leave(self, ctx, *, msg: str):
        pass

    @leave.command()
    async def enable(self, ctx):
        pass

    @leave.command()
    async def disable(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Text(bot))
