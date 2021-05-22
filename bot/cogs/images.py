from claymore import Wheel
import discord
from discord.ext import commands

from os.path import join, splitext
from glob import glob
from ntpath import basename

from PIL import Image

def collect_images(path: str):
    return { splitext(basename(img))[0]:Image.open(img).convert('RGBA') for img in glob(path) }

class Images(Wheel):
    def desc(self):
        return 'image manipluation commands'

    def __init__(self, bot):
        super().__init__(bot)

        self.images = collect_images('data/images/*.*')
        self.vince = collect_images('data/images/vince/*.*')
        self.brain = collect_images('data/images/brain/*.*')

        self.vince_range = range(2, max([int(name[0]) for name, _ in self.vince.items()]))
        self.brain_range = range(2, max([int(name[0]) for name, _ in self.brain.items()]))

    @commands.command(
        name = 'vince',
        brief = 'create a vince meme with custom text',
        usage = 'text seperated with a |'
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _vince(self, ctx, *, fields: str):
        parts = fields.split('|')

        if len(parts) not in self.vince_range:
            return await ctx.send(f'There must be between `{self.vince_range.start}` and `{self.vince_range.stop}` fields')

    @commands.command(
        name = 'brain',
        brief = 'create an expanding brain meme with custom text',
        usage = 'text seperated with a |'
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def _brain(self, ctx, *, fields: str):
        parts = fields.split('|')

        if len(parts) not in self.brain_range:
            return await ctx.send(f'There must be between `{self.brain_range.start}` and `{self.brain_range.stop}` fields')

def setup(bot):
    bot.add_cog(Images(bot))