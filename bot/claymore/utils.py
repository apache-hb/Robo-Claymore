import discord
from discord.embeds import Embed
from discord.ext import commands

from dataclasses import dataclass
import logging
from typing import Mapping

class PagedEmbed:
    def __init__(self, title: str, desc: str, colour: int = None):
        self.fields = []
        self.colour = colour
        self.title = title
        self.desc = desc

    def add_field(self, name: str, value, inline = True):
        @dataclass
        class Field:
            name: str
            value: str
            inline: bool

        self.fields.append(Field(name, value, inline))

class Context(commands.context.Context):
    def embed(self, title: str, desc: str, body: Mapping[str, str] = {}, colour: int = None) -> Embed:
        out = Embed(
            title = title,
            description = desc,
            colour = colour or self.me.color
        )

        for key, val in body.items():
            out.add_field(name = key, value = val)

        return out

    async def page_embeds(self, embed: PagedEmbed):
        fields = [embed.fields[i:i + 25] for i in range(0, len(embed.fields), 25)]

        for idx, field in zip(range(len(fields)), fields):
            page = Embed(title = embed.title, description = embed.description, colour = embed.colour)
            page.set_footer(text = f'page {idx+1} of {len(fields)}')
            for entry in field:
                page.add_field(entry.name, entry.value, inline = entry.inline)
            await self.send(embed = page)

    async def push(self, it):
        if isinstance(it, Embed):
            await self.send(embed = it)
        else:
            await self.send(it)

def wheel(visible: bool = True, desc: str = ''):
    class WheelBase(commands.Cog):
        hidden = not visible
        description = desc
        def __init__(self, bot):
            self.bot = bot
            self.db = self.bot.db
            self.log = logging.getLogger(self.__class__.__name__)

            self.log.info(f'initialized')

    return WheelBase

