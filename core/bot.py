from datetime import datetime

import discord
from discord.ext import commands


class ClayBot(commands.Bot):
    def __init__(self, command_prefix: str, activity: str, owner_id: int):
        super().__init__(
            command_prefix, 
            activity = discord.Game(activity, start = datetime.now()),
            owner_id = owner_id,
            case_insensitive = True
        )
        self.__version__ = '1.0.0'
