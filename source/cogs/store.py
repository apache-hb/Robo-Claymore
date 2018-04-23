import json
import configparser

import sys
import os

#keep this file as minimal as possible

def pyout(message: str):
    if not Store.silent: 
        print(message)
    return Store.silent
    
def add_guild(guild):
    pass

class Store:

    current_system = ''

    silent = False

    config = configparser.ConfigParser()
    config.read('./store/config.cfg')

    
