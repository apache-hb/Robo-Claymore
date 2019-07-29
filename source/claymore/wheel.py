import discord
from discord.ext import commands
import sqlite3

class Query:
    def __init__(self, db):
        self.cursor = db.cursor()
        self.query = ''
        self.db = db
        self.args = []

    def _add_part(self, part):
        self.query += part
        return self

    def where(self, name):
        return self._add_part(f'WHERE {name} ')

    def _from(self, table):
        return self._add_part(f'FROM {table} ')

    def equals(self, val):
        self._add_part('=? ')
        self.args.append(val)
        return self

    def or_replace_into(self, table):
        return self._add_part(f'OR REPLACE INTO {table}')

    def values(self, **kwargs):
        self.args += kwargs.values()
        return self._add_part('(' + ', '.join(kwargs.keys()) + ') VALUES(' + ', '.join(list('?'*len(kwargs))) + ')')

    def execute(self):
        if self.args:
            res = self.cursor.execute(self.query, tuple(self.args))
        else:
            res = self.cursor.execute(self.query)

        self.db.commit()
        return res

class Wheel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def select(self, *args):
        q = Query(self.bot.db)
        return q._add_part('SELECT ' + ', '.join(args) + ' ')

    def create(self, table):
        q = Query(self.bot.db)
        return q._add_part(f'CREATE {table} ')

    def insert(self):
        q = Query(self.bot.db)
        return q._add_part('INSERT ')

    def delete(self):
        q = Query(self.bot.db)
        return q._add_part('DELETE ')
