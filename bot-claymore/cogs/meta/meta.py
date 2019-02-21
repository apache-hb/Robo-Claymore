import json
from ..internal import Cog

class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'cog {self.__class__.__name__} loaded')

    async def on_ready(self):
        print(f'Bot loaded: {self.bot.user.name}#{self.bot.user.discriminator}')
        json.dump({
            'name': self.bot.user.name,
            'dis': self.bot.user.discriminator,
            'id': str(self.bot.user.id),
            'avatar': self.bot.user.avatar_url
        }, open('store/info.json', 'w'), indent = 4)
        #self.bot.database.cursor().execute(f"""
        #    CREATE TABLE IF NOT EXISTS bot_stats (
        #        id varchar(255) NOT NULL,
        #        dis varchar(255) NOT NULL,
        #        name varchar(255) NOT NULL
        #    ) ENGINE = ARCHIVE;
        #    
        #    INSERT INTO bot_stats (id, dis, name) 
        #    VALUES ('{self.bot.user.id}', '{self.bot.user.discriminator}', '{self.bot.user.name}');
        #    """
        #)