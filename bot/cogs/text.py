from typing import Union
from discord.ext.commands.core import group, guild_only, has_permissions
from discord import Emoji
from claymore.utils import wheel
from discord.ext.commands import command

class Text(wheel(desc = 'automatic messages')):
    def __init__(self, bot):
        super().__init__(bot)

        @bot.listen()
        async def on_message(message):
            if message.author.bot:
                return

            reacts = self.db.reacts.find_one({ 'id': message.guild.id })

            for text, emotes in (reacts or {}).items():
                if 'id' in text:
                    continue

                if text in message.content:
                    for emote in emotes:
                        await message.add_reaction(emote)

    @group()
    async def reacts(self, ctx):
        pass

    @reacts.command()
    async def add(self, ctx, emote: str, *, text: str):
        self.db.reacts.update(
            { 'id': ctx.guild.id },
            { '$set': { 'id': ctx.guild.id }, '$addToSet': { text: emote } },
            upsert = True
        )
        await ctx.send(f'will now react to `{text}` with `{emote}`')

    @reacts.command()
    async def remove(self, ctx, *, it: str):
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
