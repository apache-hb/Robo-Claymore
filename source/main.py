import sys
from typing import List

from glob import glob
from os.path import join, sep

from claymore import Claymore

def main(args: List[str]) -> None:
    bot = Claymore()
    
    for path in glob(join('cogs', '*.py')):
        bot.load_extension(path.replace(sep, '.').replace('.py', ''))
    
    bot.run('NDQ3OTIwOTk4NjIxMjQ5NTM2.XSawZA.24b0hnizTLIM780S2KIhSyvnHvs')

if __name__ == "__main__":
    main(sys.argv)