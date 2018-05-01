import discord
from discord.ext import commands

import json

from .store import Store, style_embed, pyout

class Owner:
    def __init__(self, bot):
        self.bot = bot
        pyout('Cog {} loaded'.format(self.__class__.__name__))

    short = "Owner commands"
    description = "Only the owner of the bot and whitelisted users can use these commands"
    hidden = True

    async def __local_check(self, ctx):
        if ctx.bot.is_owner(ctx.author.id):
            return True
        elif ctx.author.id in Store.whitelist:
            return True
        await ctx.send('Go away')
        return False

    @commands.group(invoke_without_command=True)
    async def whitelist(self, ctx):
        embed = style_embed(ctx, title='All whitelisted users',
        description='These people have access to special commands')
        ret=''
        if Store.whitelist:
            for a in Store.whitelist:
                user = await ctx.bot.get_user_info(a)
                ret+='{}#{}:({})\n'.format(user.name, user.discriminator, user.id)
        else:
            ret='There are no whitelisted users'
        embed.add_field(name='All users', value=ret)
        return await ctx.send(embed=embed)


    @whitelist.command(name="add")
    async def _whitelist_add(self, ctx, *, user: discord.Member):
        ret='User {} was already in the whitelist'.format(user.name)
        if user.id not in Store.whitelist:
            Store.whitelist.append(user.id)
            json.dump(Store.whitelist, open('cogs/store/whitelist.json', 'w'), indent=4)
            ret='User {} was added to the whitelist'.format(user.name)
            json.dump(Store.whitelist, open('store/whitelist.json', 'w'), indent=4)
        embed=style_embed(ctx, title='New user added to whitelist')
        embed.add_field(name='User', value=ret)
        await ctx.send(embed=embed)

    @whitelist.command(name="remove")
    async def _whitelist_remove(self, ctx, user: discord.Member):
        if user.id in Store.whitelist:
            Store.whitelist.remove(user.id)
            embed=style_embed(ctx, title='Whitelist removal')
            embed.add_field(name=user.name, value='Was removed from whitelist')
            json.dump(Store.whitelist, open('cogs/store/whitelist.json', 'w'), indent=4)
            return await ctx.send(embed=embed)
        embed=style_embed(ctx, title='Whitelist')
        embed.add_field(name=user.name,
        value='Cannot be removed from whitelist, because they are not in the whitelist')
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx):
        embed = style_embed(ctx, title='All blacklisted users',
        description='These people have been blocked from using me')
        ret=''
        if Store.blacklist:
            for a in Store.blacklist:
                user = await ctx.bot.get_user_info(a)
                ret+='{}#{}:({})\n'.format(user.name, user.discriminator, user.id)
        else:
            ret='There are no blacklisted users'
        embed.add_field(name='All users', value=ret)
        return await ctx.send(embed=embed)

    @blacklist.command(name="add")
    async def _blacklist_add(self, ctx, user: discord.Member):
        if not user.id in Store.blacklist:
            Store.blacklist.append(user.id)
            embed=style_embed(ctx, title='Blacklist addition')
            embed.add_field(name=user.name, value='Was blocked')
            json.dump(Store.blacklist, open('cogs/store/blacklist.json', 'w'), indent=4)
            return await ctx.send(embed=embed)
        embed=style_embed(ctx, title='Blacklist')
        embed.add_field(name=user.name, value='Was already blacklisted')
        return await ctx.send(embed=embed)

    @blacklist.command(name="remove")
    async def _blacklist_remove(self, ctx, user: discord.Member):
        if user.id in Store.blacklist:
            Store.blacklist.remove(user.id)
            embed=style_embed(ctx, title='Blacklist removal')
            embed.add_field(name=user.name, value='Was removed from blacklist')
            json.dump(Store.blacklist, open('cogs/store/blacklist.json', 'w'), indent=4)
            return await ctx.send(embed=embed)
        embed=style_embed(ctx, title='Blacklist')
        embed.add_field(name=user.name, 
        value='Cannot be removed from blacklist, because they are not in the blacklist')
        await ctx.send(embed=embed)

    @commands.command(name="setpresence")
    async def _setgame(self, ctx, *, name: str='Beep Boop'):
        mode = name.split(' ')[0]
        if mode.lower() == 'playing':
            activity=discord.Game(name=name)
        elif mode.lower() == 'streaming':
            activity=discord.Streaming(name=name, url='BONELESS')

        await ctx.bot.change_presence(activity=activity)
        await ctx.send('Changed presence to {}'.format(name.split()[1:]))

    @commands.command(name="setname")
    async def _setname(self, ctx, *, name: str):
        pass

    @commands.command(name="invite")
    async def _invite(self, ctx):
        await ctx.send('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=66321471'.format(ctx.bot.user.id))

    @commands.command(name="massdm")
    async def _massdm(self, ctx, *, message: str='Good day fleshy mammal'):
        for user in ctx.guild.members:
            try:
                await user.send(message)
            except Exception:
                pass

    @commands.command(name="prod")
    async def _prod(self, ctx, user: discord.Member, amt: int=50, *, message: str='Barzoople'):
        for x in range(amt):
            await user.send(message + str(x))

    @commands.command(name="serverlist")
    async def _serverlist(self, ctx):
        embed=style_embed(ctx, title='First 25 servers')
        for guild in ctx.bot.guilds[:25]:
            try:
                embed.add_field(name='{}#{}'.format(guild.name, guild.id), value=guild.create_invite(unique=False))
            except Exception:
                embed.add_field(name='{}#{}'.format(guild.name, guild.id), value='Invite creation blocked')

    @commands.command(name="echo")
    async def _echo(self, ctx, *, msg: str):
        await ctx.send(msg)

    @commands.command(name="test")
    async def _test(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Owner(bot))