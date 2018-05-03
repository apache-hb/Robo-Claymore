import discord
from discord.ext import commands

from .store import pyout, Store

class Admin:
    def __init__(self, bot):
        self.bot = bot
        pyout('Cog {} loaded'.format(self.__class__.__name__))

    @commands.command(name="kick")
    async def _kick(self, ctx, user: discord.Member):
        is_admin = ctx.author.permissions_in(ctx.channel).kick_members
        isTadmin = user.permissions_in(ctx.channel).administrator

        if ctx.author.id in Store.whitelist or self.bot.is_owner(ctx.author.id):
            is_admin = True

        if not is_admin:
            return await ctx.send('You dont have the permissions required to use the ban command')

        if isTadmin:
            return await ctx.send('I can\'t kick admins')

        if user.id == ctx.author.id:
            return await ctx.send('I can\'t kick you')

        if user.id == self.bot.user.id:
            return await ctx.send('I\'m not going to kick myself')

        if self.bot.is_owner(user.id) or user.id in Store.whitelist:
            return await ctx.send('I don\'t want to kick them')

        try:
            await user.kick()
        except discord.errors.Forbidden:
            return await ctx.send('I Don\'t have the correct permissions to do that')
        else:
            await ctx.send('He\'s gone for now')

    @commands.command(name="ban")
    async def _ban(self, ctx, user: discord.Member):
        is_admin = ctx.author.permissions_in(ctx.channel).ban_members
        isTadmin = user.permissions_in(ctx.channel).administrator

        if ctx.author.id in Store.whitelist or self.bot.is_owner(ctx.author.id):
            is_admin = True

        if not is_admin:
            return await ctx.send('You don\'t have the permissions to do that')

        if isTadmin:
            return await ctx.send('I can\'t ban other admins')

        if user.id == self.bot.user.id:
            return await ctx.send('I can\'t ban myself')

        if self.bot.is_owner(user.id) or user.id in Store.whitelist:
            return await ctx.send('I don\'t want to ban them')

        try:
            await user.ban()
        except discord.errors.Forbidden:
            return await ctx.send('I don\'t have the correct permissions to do that')
        else:
            await ctx.send('He\'s gone for good')

    @commands.command(name="prune")
    async def _prune(self, ctx, amt: int=5):
        is_admin = ctx.author.permissions_in(ctx.channel).manage_messages

        if ctx.author.id in Store.whitelist or self.bot.is_owner(ctx.author.id):
            is_admin = True

        if not is_admin:
            return await ctx.send('You don\'t have the required permissions to do that')

        if not 2 <= amt <= 100:
            return await ctx.send('Must prune between 2 and 100 messages')

        try:
            await ctx.channel.purge(limit=amt)
        except discord.errors.Forbidden:
            await ctx.send('I don\'t have the permissions to do that')
        else:
            await ctx.send('I pruned {} messages'.format(amt))

def setup(bot):
    bot.add_cog(Admin(bot))