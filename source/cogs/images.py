import discord
from aiohttp.client_exceptions import InvalidURL
from discord.ext import commands
from .utils.images import do_choice, do_note, do_button, do_kick, do_villan_image, do_retard
from .utils.converters import bytes_to_image
from .utils.networking import get_bytes

class Images:
    def __init__(self, bot):
        self.bot = bot
        print(f'Cog {self.__class__.__name__} loaded')

    @commands.command(
        name = "button"
    )
    async def _button(self, ctx, *, text: str):
        async with ctx.channel.typing():
            r = await do_button(text)
            ret = discord.File(r.getvalue(), filename = 'button.png')
            await ctx.send(file = ret)

    @commands.command(
        name = "choice"
    )
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
            if len(ctx.message.mentions) == 0:
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

            r = await do_kick(bytes_to_image(img))
            ret = discord.File(r.getvalue(), filename = 'kick.png')
            await ctx.send(file = ret)

    @commands.command(name = "words")
    async def _words(self, ctx, *, text: str):
        pass

    @commands.command(name = "prison")
    async def _prison(self, ctx, *, text: str):
        pass

    @commands.command(name = "retard")
    async def _retard(self, ctx, *, text: str):
        async with ctx.channel.typing():
            r = await do_retard(text)
            ret = discord.File(r.getvalue(), filename = 'retard.png')
            await ctx.send(file = ret)

    @commands.command(name = "shout")
    async def _shout(self, ctx, *, text: str):
        pass

    @commands.command(name = "tweet")
    async def _tweet(self, ctx, *, text: str):
        pass

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

def setup(bot):
    bot.add_cog(Images(bot))