from glob import glob
from os.path import join
from os import sep
import json

import discord
from discord.ext import commands

class Claymore(commands.Bot):
    COG_GLOB = join('cogs', '*.py')
    I18N_GLOB = join('i18n', '*.json')

    def __init__(self, prefix: str, activity: str, owner: int, config: dict):
        super().__init__(
            prefix, 
            activity = discord.Game(activity),
            owner_id = owner,
            case_insensitive = True
        )
        self.__version__ = '0.5.0'

    def load_cogs(self):
        for cog in glob(self.COG_GLOB):
            
            if '__init__' in cog:
                continue

            try:
                self.load_extension(cog.replace(sep, '.')[:-3])
            except Exception as e:
                print(f'failed to load cog {e}')

if __name__ == '__main__':
    bot = Claymore('!!', '!!testing', 0, None)
    bot.load_cogs()
    bot.run('[todo]')
