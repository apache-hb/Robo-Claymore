import discord
from aiohttp.client_exceptions import InvalidURL
from discord.ext import commands

from .utils.converters import bytes_to_image
from .utils.images import (
    do_button, do_choice,
    do_kick, do_note, do_retard,
    do_villan_image, do_words,
    do_prison, do_shout, do_tweet,
    do_rtx, do_wack, do_crusade,
    do_violation
)
from .utils.networking import get_bytes
from .utils.filters import do_deepfry, jpegify, do_sharpen, emboss
from io import BytesIO

HAMMER = open('cogs/images/banhammer.jpg', 'rb')
BANHAMMER = discord.File(HAMMER, 'banhammer.jpg')

SHAD = open('cogs/images/shadman.png', 'rb')
SHADMAN = discord.File(SHAD, 'shadman.png')


async def message_check(ctx):
    if '>shadman' in ctx.content:
        await ctx.channel.send(file = SHADMAN)
    elif 'b&' in ctx.content:
        await ctx.channel.send(file = BANHAMMER)

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_listener(message_check, 'on_message')
        print(f'Cog {self.__class__.__name__} loaded')

    @commands.command(
        name = "emboss"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _emboss(self, ctx, text: str):
        async with ctx.channel.typing():
            try:
                ret = await get_bytes(text)
            except InvalidURL:
                return await ctx.send('Invalid URL')
            ret = await emboss(bytes_to_image(ret))
            f = discord.File(ret.getvalue(), filename = 'emboss.png')
            return await ctx.send(file = f)

    @commands.command(
        name = "sharpen"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _sharpen(self, ctx, text: str):
        async with ctx.channel.typing():
            try:
                img = await get_bytes(text)
            except InvalidURL:
                return await ctx.send('Invalid URL')

            ret = await do_sharpen(bytes_to_image(img))
            f = discord.File(ret.getvalue(), filename = 'sharpen.png')
            await ctx.send(file = f)

    @commands.command(
        name = "jpeg",
        aliases = ['needsmorejpeg', 'jpegify']
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _jpeg(self, ctx, text: str):
        async with ctx.channel.typing():
            try:
                img = await get_bytes(text)
            except InvalidURL:
                return await ctx.send('Invalid URL')
            ret = await jpegify(bytes_to_image(img))
            f = discord.File(ret.getvalue(), filename = 'jpegified.jpeg')
            await ctx.send(file = f)

    @commands.command(
        name = "deepfry"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _deepfry(self, ctx, text: str):
        async with ctx.channel.typing():
            try:
                img = await get_bytes(text)
            except InvalidURL:
                return await ctx.send('Invalid URL')
            ret = await do_deepfry(bytes_to_image(img))
            f = discord.File(ret.getvalue(), filename = 'deepfry.png')
            await ctx.send(file = f)

    @commands.command(
        name = "button",
        description = "press a button with some text on it",
        brief = "its a blue button"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _button(self, ctx, *, text: str):
        async with ctx.channel.typing():
            r = await do_button(text)
            ret = discord.File(r.getvalue(), filename = 'button.png')
            await ctx.send(file = ret)

    @commands.command(
        name = "choice"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _choice(self, ctx, *, text: str):
        split = text.split('|')
        async with ctx.channel.typing():
            try:
                f = await do_choice(split[0], split[1])
            except IndexError:
                return await ctx.send('you need to provide two peices of text (split it with `|`)')

            ret = discord.File(f.getvalue(), filename = 'choice.png')
            await ctx.send(file = ret)

    @commands.command(
        name = "note"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _note(self, ctx, *, text: str):
        async with ctx.channel.typing():
            f = await do_note(text)
            ret = discord.File(f.getvalue(), filename = 'note.png')
            await ctx.send(file = ret)

    @commands.command(
        name = "doorkick"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _doorkick(self, ctx, image):
        async with ctx.channel.typing():
            if not ctx.message.mentions:
                try:
                    img = await get_bytes(image)
                except InvalidURL:
                    return await ctx.send('thats not a valid url')
            else:
                #must be a mention for a user
                try:
                    img = await get_bytes(ctx.message.mentions[0].avatar_url)
                except IndexError:
                    return await ctx.send('must either be url or a user mention')
            try:
                r = await do_kick(bytes_to_image(img))
            except OSError:
                return await ctx.send('I dont know what that is, but it isnt an image i can use')
            ret = discord.File(r.getvalue(), filename = 'kick.png')
            await ctx.send(file = ret)

    @commands.command(name = "firstwords")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _words(self, ctx, *, text: str):
        async with ctx.channel.typing():
            r = await do_words(text)
            ret = discord.File(r.getvalue(), filename = 'words.png')
            await ctx.send(file = ret)

    @commands.command(name = "prison")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _prison(self, ctx, *, text: str):
        async with ctx.channel.typing():
            r = await do_prison(text)
            ret = discord.File(r.getvalue(), filename = 'prison.png')
            await ctx.send(file = ret)

    @commands.command(name = "retard")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _retard(self, ctx, *, text: str):
        async with ctx.channel.typing():
            r = await do_retard(text)
            ret = discord.File(r.getvalue(), filename = 'retard.png')
            await ctx.send(file = ret)

    @commands.command(name = "shout")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _shout(self, ctx, first: discord.User, second: discord.User):
        async with ctx.channel.typing():
            f = await get_bytes(first.avatar_url)
            s = await get_bytes(second.avatar_url)
            r = await do_shout(bytes_to_image(f), bytes_to_image(s))
            ret = discord.File(r.getvalue(), filename = 'shout.png')
            await ctx.send(file = ret)

    @commands.command(name = "tweet")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _tweet(self, ctx, *, text: str):
        async with ctx.channel.typing():
            r = await do_tweet(text)
            ret = discord.File(r.getvalue(), filename = 'tweet.png')
            await ctx.send(file = ret)

    @commands.command(name = "villan")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def _villan(self, ctx, *, text: str):
        async with ctx.channel.typing():
            if len(ctx.message.mentions) == 2:
                first = await get_bytes(ctx.message.mentions[0].avatar_url)
                second = await get_bytes(ctx.message.mentions[1].avatar_url)
            else:
                txt = text.split('|')
                try:
                    first = await get_bytes(txt[0])
                    second = await get_bytes(txt[1])
                except IndexError:
                    return await ctx.send('you need to provide 2 urls or 2 users')
                except InvalidURL:
                    return await ctx.send('one of those was not a valid url')

            r = await do_villan_image(bytes_to_image(first), bytes_to_image(second))
            ret = discord.File(r.getvalue(), filename = 'villan.png')
            await ctx.send(file = ret)

    @commands.command(name = "rtx")
    async def _rtx(self, ctx, first: str, second: str):
        async with ctx.channel.typing():
            if len(ctx.message.mentions) == 2:
                f = await get_bytes(ctx.message.mentions[0].avatar_url)
                s = await get_bytes(ctx.message.mentions[1].avatar_url)
            else:
                try:
                    f = await get_bytes(first)
                    s = await get_bytes(second)
                except InvalidURL:
                    return await ctx.send('one of those urls was not valid')
            r = await do_rtx(bytes_to_image(f), bytes_to_image(s))
            ret = discord.File(r.getvalue(), filename = 'rtx.png')
            await ctx.send(file = ret)

    @commands.command(name = "wack")
    async def _wack(self, ctx, user: discord.User):
        async with ctx.channel.typing():
            img = await get_bytes(user.avatar_url)
            r = await do_wack(bytes_to_image(img))
            ret = discord.File(r.getvalue(), filename = 'wack.png')
            await ctx.send(file = ret)

    @commands.command(name = "crusade")
    async def _crusade(self, ctx, first: str):
        async with ctx.channel.typing():
            if ctx.message.mentions:
                img = await get_bytes(ctx.message.mentions[0].avatar_url)
            else:
                try:
                    img = await get_bytes(first)
                except InvalidURL:
                    return await ctx.send('Invalid URL')
            r = await do_crusade(bytes_to_image(img))
            ret = discord.File(r.getvalue(), filename = 'crusade.png')
            await ctx.send(file = ret)

    @commands.command(name = "violation")
    async def _violation(self, ctx, *, text: str):
        async with ctx.channel.typing():
            r = await do_violation(text)
            ret = discord.File(r.getvalue(), filename = 'violation.png')
            await ctx.send(file = ret)

def setup(bot):
    bot.add_cog(Images(bot))
