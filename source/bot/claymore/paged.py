import discord

class PagedEmbed:
    def __init__(self, title: str, description: str, colour: int = 0x023cfc):
        self.fields = []
        self.colour = colour
        self.title = title
        self.description = description

    def add_field(self, name, value, inline = True):
        self.fields.append((name, value, inline))
        