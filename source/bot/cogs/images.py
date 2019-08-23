from claymore import Wheel
import discord
from discord.ext import commands

from os.path import join, splitext
from glob import glob
from ntpath import basename

from PIL import Image

class Images(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

        images_path = join('..', 'data', 'images', '*.*')
        self.images = {splitext(basename(img))[0]:Image.open(img).convert('ARGB') for img in glob(images_path)}

        vince_path = join('..', 'data', 'images', 'vince', '*.*')
        self.vince = {splitext(basename(img))[0]:Image.open(img).convert('ARGB') for img in glob(vince_path)}
        self.vince_range = range(2, max([name[0] for name, _ in self.vince.items()]))

        brains_path = join('..', 'data', 'images', 'brain', '*.*')
        self.brain = {splitext(basename(img))[0]:Image.open(img).convert('ARGB') for img in glob(brains_path)}
        self.brain_range = range(2, max([name[0] for name, _ in self.brain.items()]))

    @commands.command(name = 'vince')
    @commands.cooldown(1, 15, commands.BucketType.user)
    def _vince(self, ctx, *, fields: str):
        pass

    @commands.command(name = 'brain')
    @commands.cooldown(1, 15, commands.BucketType.user)
    def _brain(self, ctx, *, fields: str):
        pass

def setup(bot):
    bot.add_cog(Images(bot))