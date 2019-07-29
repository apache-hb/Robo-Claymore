from discord.ext import commands
import sqlite3
import json
from .context import Context as ClayContext
from os.path import join

class Claymore(commands.Bot):
    async def get_prefix(self, msg):
        res = self.query(f'SELECT prefix FROM custom_prefixes WHERE id = ?', (msg.guild.id,)).fetchone()
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

        self.config = json.load(open(join('data', 'config.json'), 'r'))
        self.owner = int(self.config['discord']['owner'])

        # connect to the database, will be created if it doesnt exist
        self.db = sqlite3.connect(join('data', 'claymore.db'))
        cur = self.db.cursor()

    def cleanup(self):
        self.close()
        self.db.commit()
        self.db.close()

    def get_context(self, msg, *, cls=ClayContext):
        return super().get_context(msg, cls=cls)