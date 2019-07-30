from discord.ext import commands
import sqlite3
import json
from .context import Context as ClayContext
from os.path import join, abspath, dirname, isfile
from os import access, R_OK

def get_config():
    path = join('data', 'config.json')
    if isfile(path) and access(path, R_OK):
        return json.load(open(path, 'r'))
    else:
        data = {
            'discord': {
                'token': input('Input discord bot token'),
                'owner': int(input('Input owner id')),
                'prefix': input('Input default prefix')
            }
        }

        json.dump(data, open(path, 'w'), indent = 4)
        return data


class Claymore(commands.Bot):
    async def get_prefix(self, msg):
        try:
            res = self.query(f'SELECT prefix FROM custom_prefixes WHERE id = ?', (msg.guild.id,)).fetchone()
        except sqlite3.ProgrammingError:
            res = None

        prefix = self.config['discord']['prefix']
        if res is None:
            return prefix

        return (res[0], prefix)

    def execute(self, query: str):
        cur = self.db.cursor()
        res = cur.execute(query)
        self.db.commit()
        return res

    def query(self, query: str, args: tuple):
        cur = self.db.cursor()
        res = cur.execute(query, args)
        self.db.commit()
        return res

    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True
        )
        self.config = get_config()
        self.owner = self.config['discord']['owner']

        # connect to the database, will be created if it doesnt exist
        self.db = sqlite3.connect(join('data', 'claymore.db'))
        cur = self.db.cursor()

    async def cleanup(self):
        await self.close()
        self.db.commit()
        self.db.close()

    def run(self):
        super().run(self.config['discord']['token'])

    def get_context(self, msg, *, cls=ClayContext):
        return super().get_context(msg, cls=cls)