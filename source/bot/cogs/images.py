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

        brains_path = join('..', 'data', 'images', 'brain', '*.*')
        self.brain = {splitext(basename(img))[0]:Image.open(img).convert('ARGB') for img in glob(brains_path)}

def setup(bot):
    bot.add_cog(Images(bot))