from discord.ext.commands import group, command
from claymore.utils import wheel
from asyncpraw import Reddit

class Media(wheel(desc = 'social media websites')):
    def __init__(self, bot):
        super().__init__(bot)

        if rcfg := bot.config.get('reddit', None):
            self.rapi = Reddit(
                client_id = rcfg['id'],
                client_secret = rcfg['secret'],
                user_agent = 'python:discord.claymore:v2'
            )
        else:
            self.reddit.update(enabled = False)
            self.log.warning('reddit keys not configured, disabling command')

    #TODO: all of these
    @group()
    async def reddit(self, ctx, sub: str = 'all', search: str = 'hot', idx: int = None):
        res = await self.rapi.subreddit(sub)


    @reddit.command(
        name = 'subscribe'
    )
    async def reddit_subscribe(self, ctx, guild: str):
        pass



    @command()
    async def ruqqus(self, ctx, post: str):
        pass



    @group()
    async def twitter(self, ctx):
        pass

    @twitter.command(
        name = 'follow'
    )
    async def twitter_follow(self, ctx, user: str):
        pass

def setup(bot):
    bot.add_cog(Media(bot))
    