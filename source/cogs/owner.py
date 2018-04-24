import discord
from discord.ext import commands

from .store import Store, style_embed

class Owner:
    def __init__(self, bot):
        self.bot = bot
        print('Cog {} loaded'.format(self.__class__.__name__))
    
    short = "Owner commands"
    description = "Only the owner of the bot and whitelisted users can use these commands"
    hidden = True

    async def __local_check(self, ctx):
        if ctx.bot.is_owner(ctx.author.id):
            return True
        elif ctx.author.id in []:#todo, whitelist and blacklist
            return True
        await ctx.send('Fuck off')
        return False

    @commands.group(invoke_without_command=True)
    async def whitelist(self, ctx):
        embed = style_embed(ctx, title='All whitelisted users', 
        description='These people have access to special commands')
        ret=''
        if Store.whitelist:
            for a in Store.whitelist:
                user = ctx.bot.get_user_info(a)
                ret+=user.name+'#'+user.discriminator+':('+user.id+')\n'
        else:
            ret='There are no whitelisted users'
        embed.add_field(name='All users', value=ret)
        return await ctx.send(embed=embed)


    @whitelist.command(name="add")
    async def _add(self, ctx, user: discord.Member):
        pass

    @whitelist.command(name="remove")
    async def _remove(self, ctx, user: discord.Member):
        pass

    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx):
        pass

    @blacklist.command(name="add")
    async def _add(self, ctx, user: discord.Member):
        pass

    @blacklist.command(name="remove")
    async def _removes(self, ctx, user: discord.Member):
        pass

    @commands.command(name="echo")
    async def _echo(self, ctx, *, msg: str=None):
        pass

    @commands.command(name="test")
    async def _test(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Owner(bot))