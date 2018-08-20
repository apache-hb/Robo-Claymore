from discord.ext import commands

async def can_override(ctx, user = None):
    if user is None:
        user = ctx.author #TODO: add whitelist
    return await ctx.bot.is_owner(user) #or user.id in whitelist

def is_admin():
    async def predicate(ctx):
        if ctx.author.permissions_in(ctx.channel).administrator or await can_override(ctx):
            return True
        await ctx.send('You dont have the required admin permissions')
        return False
    return commands.check(predicate)

def can_kick():
    async def predicate(ctx):
        if ctx.author.permissions_in(ctx.channel).kick_members or await can_override(ctx):
            return True
        await ctx.send('You dont have the permission to kick')
        return False
    return commands.check(predicate)

def can_ban():
    async def predicate(ctx):
        if ctx.author.permissions_in(ctx.channel).ban_members or await can_override(ctx):
            return True
        await ctx.send('You dont have the permission to ban')
        return False
    return commands.check(predicate)

def manage_messages():
    async def predicate(ctx):
        if ctx.author.permissions_in(ctx.channel).manage_messages or await can_override(ctx):
            return True
        await ctx.send('You dont have the permission to delete messages')
        return False
    return commands.check(predicate)

def manage_nicknames():
    async def predicate(ctx):
        if ctx.author.permissions_in(ctx.channel).manage_nicknames or await can_override(ctx):
            return True
        await ctx.send('You dont have the permission to manage nicknames')
        return False
    return commands.check(predicate)
