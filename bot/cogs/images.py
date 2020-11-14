from claymore.utils import wheel
from claymore.net import json_request

from discord import File
from discord.ext.commands import command

from io import BytesIO
from glob import glob
from random import choice

class Images(wheel(desc = 'image manipulation')):
    def __init__(self, bot):
        super().__init__(bot)

        self.frothy_images = glob('images/frothy/*.png')

    @command(
        brief = 'the scrub mentality',
        help = """
        // get a random picture of frothy omen
        &frothy

        // get a specific picture of frothy omen
        &frothy 0
        """
    )
    async def frothy(self, ctx, idx: int = None):
        if not idx:
            await ctx.send(file = File(choice(self.frothy_images)))
        elif idx not in range(len(self.frothy_images)):
            await ctx.send(f'index must be between 0 and {len(self.frothy_images)}')
        else:
            await ctx.send(file = File(self.frothy_images[idx]))
        
    @command(
        brief = 'get a picture of a cat',
        help = """
        // get a cat picture from the internet
        &cat
        """
    )
    async def cat(self, ctx):
        obj = await json_request('https://api.thecatapi.com/v1/images/search')
        return await ctx.send(embed = ctx.embed('cat', 'thecatapi.com', image = obj[0]['url']))

def setup(bot):
    bot.add_cog(Images(bot))