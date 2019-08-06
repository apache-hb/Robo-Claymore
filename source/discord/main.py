import sys
from typing import List

from glob import glob
from os.path import join, sep, isfile, abspath, dirname
from os import access, R_OK

from claymore import Claymore
import json

def main(args: List[str]) -> None:
    bot = Claymore()

    for path in glob(join('discord', 'cogs', '*.py')):
        bot.load_extension(path.replace(sep, '.').replace('.py', '').replace('discord.', ''))

    bot.run()

if __name__ == "__main__":
    main(sys.argv)