import discord
from discord.ext import commands

class Context(commands.context.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_embed(self, title, description, colour = 0x023cfc) -> discord.Embed:
        try:
            colour = self.me.colour
        except AttributeError:
            pass
        return discord.Embed(title = title, description = description, colour = colour)

    async def send_pages(self, content):
        fields = [content.fields[i:i + 25] for i in range(0, len(content.fields), 25)]
        for idx, each in zip(range(len(fields)), fields):
            embed = discord.Embed(title = content.title, description = content.description, colour = content.colour)
            embed.set_footer(text = f'page {idx+1} of {len(fields)}')
            for field in each:
                embed.add_field(name = field[0], value = field[1], inline = field[2])
            await self.send(embed = embed)
