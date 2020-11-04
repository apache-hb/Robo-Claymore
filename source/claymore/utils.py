import discord
from discord.ext import commands

from dataclasses import dataclass
import logging

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

class ClayContext(commands.context.Context):
    async def page_embeds(self, embed: PagedEmbed):
        fields = [embed.fields[i:i + 25] for i in range(0, len(embedfields), 25)]

        for idx, field in zip(range(len(fields)), fields):
            page = discord.Embed(title = embed.title, description = embed.description, colour = embed.colour)
            page.set_footer(text = f'page {idx+1} of {len(fields)}')
            for entry in field:
                page.add_field(entry.name, entry.value, inline = entry.inline)
            await self.send(embed = page)

class Wheel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.db[self.bot.config['mongo']['db']]
        self.log = logging.getLogger(self.__class__.__name__)

        self.log.info(f'initialized')
