from datetime import datetime

import discord
from discord.ext import commands

import mysql.connector

class ClayBot(commands.Bot):
    def __init__(self, command_prefix: str, activity: str, owner_id: int, sql_name: str, sql_pass: str):
        super().__init__(
            command_prefix, 
            activity = discord.Game(activity, start = datetime.now()),
            owner_id = owner_id,
            case_insensitive = True
        )
        self.__version__ = '1.0.0'
        
        self.database = mysql.connector.connect(
            host = 'localhost',
            user = sql_name,
            password = sql_pass,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.database.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS `claymore`;")
