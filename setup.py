#this is empty for now so pip doesnt complain when updating
#TODO pip is still fucking complaining
#if you want to run the bot just check inside /source and run the script called runself
#python3 runself.py

import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

def ensure_file(ensure: str, default: str):
    if not os.path.isfile(ensure):
        file = open(ensure, 'w')
        file.write(default)
        file.close()
        return True
    return False

if not os.path.exists(os.path.join(dir_path, 'source/cogs/store')):
    os.mkdir(os.path.join(dir_path, 'source/cogs/store'))

if ensure_file('./source/cogs/store/bot.log', 'logging file \n'):
    print('logfile was generated')

if ensure_file('./source/cogs/store/direct.log', 'direct messages file \n'):
    print('direct messages was generated')

statistic_dict = {
    "messages_processed": 0,
    "commands_used": 0
}

if ensure_file('./source/cogs/store/statistics.json', json.dumps(statistic_dict, indent=4)):
    print('statistics file was generated')

if ensure_file('./source/cogs/store/symbiosis.json', '[]'):
    print('symbiosis file was generated')

if ensure_file('./source/cogs/store/tags.json', '[]'):
    print('tags file was generated')

if ensure_file('./source/cogs/store/quotes.json', '[]'):
    print('quotes file was generated')

if ensure_file('./source/cogs/store/autoreact.json', '[]'):
    print('autoreact file was generated')

if ensure_file('./source/cogs/store/autorole.json', '[]'):
    print('autorole file was generated')

if ensure_file('./source/cogs/store/disabled.json', '[]'):
    print('disabled file was generated')

if ensure_file('./source/cogs/store/blacklist.json', '[]'):
    print('blacklist file was generated')

if ensure_file('./source/cogs/store/blocked.json', '[]'):
    print('blocked file was generated')

if ensure_file('./source/cogs/store/whitelist.json', '[]'):
    print('whitelist file was generated')

if ensure_file('./source/cogs/store/welcome.json', '[]'):
    print('welcome file was generated')

if ensure_file('./source/cogs/store/leave.json', '[]'):
    print('leave file was generated')