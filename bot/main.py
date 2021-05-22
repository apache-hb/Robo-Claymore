from typing import List

from glob import glob
from os.path import sep, isfile, abspath, dirname, join, splitext
from os import access, R_OK
from pathlib import Path

from claymore import Claymore
import json

import logging
import sys
import argparse

parser = argparse.ArgumentParser(description = 'discord bot')

parser.add_argument('--config',
    help = 'path to config file',
    nargs = '?', default = 'data/config.ini',
    type = str
)

parser.add_argument('--cogs',
    help = 'path to cogs folder',
    nargs = '?', default = Path('cogs'),
    type = Path
)

def clean_path(path: str) -> str:
    path = splitext(path)[0]
    
    for ch in [ '/', '\\' ]:
        path = path.replace(ch, '.')

    return path.replace('bot.', '')


def main():
    # setup logging to log to stdout
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(name)s:%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # parse args    
    args = parser.parse_args()

    bot = Claymore(args.config)

    bot.log.info(f'loading all cogs in `{args.cogs}`')

    for path in glob('bot/cogs/*.py'):
        mod = clean_path(path)
        bot.load_extension(mod)

    bot.run()

if __name__ == "__main__":
    main()
