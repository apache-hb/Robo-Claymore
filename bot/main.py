from os.path import splitext
from pathlib import Path

from claymore import Claymore

import logging
import sys
import argparse
import asyncio
import traceback

parser = argparse.ArgumentParser(description = 'discord bot')

parser.add_argument('--config',
    help = 'path to config file',
    nargs = '?', default = 'data/config.toml',
    type = str
)

parser.add_argument('--cogs',
    help = 'path to cogs folder',
    nargs = '?', default = Path('bot/cogs'),
    type = Path
)

def clean_path(path: str) -> str:
    path = splitext(path)[0]
    
    for ch in [ '/', '\\' ]:
        path = path.replace(ch, '.')

    return path.replace('bot.', '')

def make_bot(config):
    # setup logging to log to stdout
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(name)s:%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    return Claymore(config)

async def main(bot, cogs):
    bot.log.info(f'loading all cogs in `{cogs}`')

    for path in cogs.glob('*.py'):
        mod = clean_path(path)
        try:
            await bot.load_extension(mod)
        except Exception:
            logging.exception(f'failed to load cog `{mod}`')

if __name__ == "__main__":
    args = parser.parse_args()

    bot = make_bot(args.config)
    asyncio.run(main(bot, args.cogs))
    bot.run()
