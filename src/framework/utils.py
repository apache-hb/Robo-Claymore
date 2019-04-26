import discord

def embed(ctx, title: str, description: str = None, colour: int = 0x023cfc) -> discord.Embed:
    try: 
        colour = ctx.me.colour
    except AttributeError:
        pass
    
    return discord.Embed(title = title, description = description, colour = colour)
