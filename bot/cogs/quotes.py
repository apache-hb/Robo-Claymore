from claymore import Wheel, PagedEmbed
import discord
from discord.ext import commands
from random import choice

class Quotes(Wheel):
    def desc(self):
        return 'dont quote me on that'

    @commands.group(
        name = 'quote',
        brief = 'get a server quote',
        invoke_without_command = True
    )
    @commands.guild_only()
    async def _quote(self, ctx, index: int = None):
        quotes = await self.db.quotes.find_one({ 'id': ctx.guild.id })

        if quotes is None or not 'quotes' in quotes or not quotes['quotes']:
            return await ctx.send('This server has no quotes')

        if index is None:
            return await ctx.send(choice(quotes['quotes']))

        try:
            await ctx.send(quotes['quotes'][index])
        except IndexError:
            await ctx.send(f'No quote at index {index}')

    @_quote.command(
        name = 'add',
        brief = 'add a tag with content'
    )
    async def _quote_add(self, ctx, *, text: str):
        await self.db.quotes.update(
            { 'id': ctx.guild.id },
            { '$push': { 'quotes': text } },
            upsert = True
        )

        quotes = await self.db.quotes.find_one({ 'id': ctx.guild.id })

        await ctx.send(f'Added quote with an index of {len(quotes["quotes"])-1}')

    @_quote.command(
        name = 'remove',
        brief = 'remove a tag'
    )
    async def _quote_remove(self, ctx, index: int):
        await self.db.quotes.update(
            { 'id': ctx.guild.id },
            { '$unset': { f'quotes.{index}': 1 } },
            upsert = True
        )

        await self.db.quotes.update(
            { 'id': ctx.guild.id },
            { '$pull': { 'quotes': None } }
        )

        await ctx.send(f'Removed quote at {index} if there was one')

    #TODO: broken
    @_quote.command(
        name = 'list',
        brief = 'list all quotes for the current server'
    )
    async def _quote_list(self, ctx):
        quotes = await self.db.quotes.find_one({ 'id': ctx.guild.id })

        if quotes is not None or 'quotes' not in quotes:
            return await ctx.send('This server has no quotes')

        embed = PagedEmbed(f'All quotes for {ctx.guild.name}', f'{len(quotes["quotes"])} total')

        for idx, each in enumerate(quotes['quotes']):
            embed.add_field(name = f'Quote {idx}', value = each, inline = False)

        await ctx.send_pages(embed)

    @_quote.command(
        name = 'purge',
        brief = 'remove all tags from the current server',
        aliases = [ 'wipe', 'clean', 'reset' ]
    )
    @commands.has_permissions(administrator = True)
    async def _quote_purge(self, ctx):
        await self.db.quotes.remove({ 'id': ctx.guild.id })
        await ctx.send('Removed all quotes')

def setup(bot):
    bot.add_cog(Quotes(bot))