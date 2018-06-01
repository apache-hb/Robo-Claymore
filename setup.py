import os
import json

if not os.path.isdir('source/cogs/store'):
    os.mkdir('soruce/cogs/store')

print('{:=^50}'.format('Robo Claymore setup script'))
print('{:^50}'.format('To skip a token, just press enter'))

default = {
    'discord': {
        'token': input('(required) input your discord bot token\n'),
        'prefix': input('(required) input your bots desired prefix\n'),
        'activity': input('(optional) input the bots default activity\n'),
        'description': input('(optional) input the help flavor text\n'),
        'owner': input('(optional) input your own user id so the bot can know who you are\n')
    },
    'fortnite': {
        'key': input('(optional) input a fortnite bot key to enable the fortnite commands\n')
    },
    'wolfram': {
        'key': input('(optional) input a wolfram alpha key to enable the wolfram command\n')
    },
    'fortnite': {
        'key': input('(optional) input a fortnite key to enable fortnite support\n')
    },
    'disabled': {
        'cogs': [

        ],
        'commands': [

        ]
    }
}

json.dump(default, open('source/cogs/store/config.json', 'w'), indent = 4)

files = [
    'whitelist',
    'blacklist',
    'logs'
]

for a in files:
    if not os.path.isfile('source/cogs/store/{}.json'.format(a)):
        b = open('source/cogs/store/{}.json'.format(a), 'w')
        b.write('[]')
        b.close()
        print('{} file was generated'.format(a))