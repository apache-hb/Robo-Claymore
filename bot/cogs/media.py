from discord.ext.commands import group, command
from claymore.utils import wheel

class Media(wheel(desc = 'social media websites')):
    @group()
    async def reddit(self, ctx):
        pass

    @reddit.command()
    async def reddit_subscribe(self, ctx, guild: str):
        pass



    @command()
    async def ruqqus(self, ctx, post: str):
        pass



    @group()
    async def twitter(self, ctx):
        pass

    @twitter.command()
    async def twitter_follow(self, ctx, user: str):
        pass

def setup(bot):
    bot.add_cog(Media(bot))
    