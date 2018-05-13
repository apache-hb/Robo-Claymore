import os
import json

# for making sure a file exists
# ensure is the name of the file to check for existence
# default is the default content to preint to it if it doesnt exist


def ensure_file(ensure: str, default):
    if not os.path.isfile(ensure):
        file = open(ensure, 'w')
        file.write(default)
        file.close()
        print('File {} was generated'.format(ensure))


stats = {'total_commands': 0, 'total_messages': 0}

print('''
+---------------------------------------------------------------+
|   welcome to the setup for robo claymore                      |
|   the discord token and prefix are the only mandatory inputs  |
|   all the other tokens can be skipped by entering nothing     |
+---------------------------------------------------------------+
''')

config = {
    'discord': {
        'token': input('input discord token\n'),
        'prefix': input('input discord prefix\n'),
        'activity': input('input default discord activity\n'),
        'description': input('input bot description\n')
    },
    'fortnite': {
        'launcher_token': input('input fortnite launcher token\n'),
        'user_token': input('input fortnite user token\n'),
        'password': input('input fortnite password\n'),
        'email': input('input fortnite email\n')
    },
    'wolfram': {
        'key': input('input wolfram key\n')
    }
}

# TODO there must be a way to do this with reflection
store_files = [
    {'name': 'tag', 'default': '[]'},
    {'name': 'quote', 'default': '[]'},
    {'name': 'autoreact', 'default': '[]'},
    {'name': 'leave', 'default': '[]'},
    {'name': 'join', 'default': '[]'},
    {'name': 'autorole', 'default': '[]'},
    {'name': 'blocked', 'default': '[]'},
    {'name': 'whitelist', 'default': '[]'},
    {'name': 'blacklist', 'default': '[]'},
    {'name': 'config', 'default': json.dumps(config, indent=4)},
    {'name': 'stats', 'default': json.dumps(stats, indent=4)}
]

if not os.path.isdir('source/cogs/store'):
    os.mkdir('source/cogs/store')
    print('store file was made')

for a in store_files:
    if not os.path.isfile('source/cogs/store/' + a['name'] + '.json'):
        file = open('source/cogs/store/' + a['name'] + '.json', 'w')
        file.write(a['default'])
        file.close()
        print('{} file was generated'.format(a['name']))

json.dump(config, open('source/cogs/store/config.json', 'w'), indent=4)