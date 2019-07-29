import sys
from typing import List

from glob import glob
from os.path import join, sep

from claymore import Claymore

def get_config():
    return json.load(open(join('data', 'config.json'), 'r'))

def main(args: List[str]) -> None:
    bot = Claymore()
    
    for path in glob(join('cogs', '*.py')):
        bot.load_extension(path.replace(sep, '.').replace('.py', ''))
    
    config = get_config()

    bot.run(config['discord']['token'])

if __name__ == "__main__":
    main(sys.argv)