import json

import uvloop

from core import ClayBot
from glob import glob

def get_config():
    try:
        return json.load(open('store/config.json'))
    except FileNotFoundError:
        config = {
            'token': input('Bot token: '),
            'prefix': input('Default bot prefix: '),
            'activity': input('Default bot activity: '),
            'owner': int(input('Owner discord ID')),
            'sql': {
                'name': input('Input sql name'),
                'pass': input('Input sql password')
            }
        }
        json.dump(config, open('store/config.json', 'w'), indent = 4)
        return config

def main():
    #install uvloop to speed up the event loop
    uvloop.install()

    config: dict = get_config()

    bot = ClayBot(
        config['prefix'], 
        config['activity'], 
        config['owner'], 
        config['sql']['name'], 
        config['sql']['pass']
    )

    for cog in glob('cogs/*'):
        #skip everything with __ in it
        if '__' in cog:
            continue

        name = cog.replace('/', '.') + '.__init__'

        try:
            bot.load_extension(name)
        except Exception as e:
            print(f'{cog} failed to load: {e}')

    bot.run(config['token'])

if __name__ == '__main__':
    main()
