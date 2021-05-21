from typing import List

from glob import glob
from os.path import sep, isfile, abspath, dirname
from os import access, R_OK

from claymore import Claymore
import json

def main():
    bot = Claymore()

    for path in glob('cogs/*.py'):
        bot.load_extension(path.replace(sep, '.').replace('.py', '').replace('discord.', ''))

    bot.run()

if __name__ == "__main__":
    main()
