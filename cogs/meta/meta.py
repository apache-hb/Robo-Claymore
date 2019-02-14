
from ..__utils import Cog

class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'cog {self.__class__.__name__} loaded')
