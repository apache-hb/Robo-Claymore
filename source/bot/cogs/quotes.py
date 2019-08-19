from claymore import Wheel, PagedEmbed
import discord
from discord.ext import commands
from random import choice

class Quotes(Wheel):
    @commands.group(
        name = 'quote',
        invoke_without_command = True
    )
    @commands.guild_only()
    async def _quote(self, ctx, index: int = None):
        quotes = self.db.quotes.find_one({ 'id': ctx.guild.id })

        if quotes is None or not 'quotes' in quotes or not quotes['quotes']:
            return await ctx.send('This server has no quotes')

        if index is None:
            return await ctx.send(choice(quotes['quotes']))

        try:
            await ctx.send(quotes['quotes'][index])
        except IndexError:
            await ctx.send(f'No quote at index {index}')

    @_quote.command(name = 'add')
    async def _quote_add(self, ctx, *, text: str):
        self.db.quotes.update(
            { 'id': ctx.guild.id },
            { '$push': { 'quotes': text } },
            upsert = True
        )

        quotes = self.db.quotes.find_one({ 'id': ctx.guild.id })

        await ctx.send(f'Added quote with an index of {len(quotes["quotes"])-1}')

    @_quote.command(name = 'remove')
    async def _quote_remove(self, ctx, index: int):
        self.db.quotes.update(
            { 'id': ctx.guild.id },
            { '$unset': { f'quotes.{index}': 1 } },
            upsert = True
        )

        self.db.quotes.update(
            { 'id': ctx.guild.id },
            { '$pull': { 'quotes': None } }
        )

        await ctx.send(f'Removed quote at {index} if there was one')

    @_quote.command(name = 'list')
    async def _quote_list(self, ctx):
        quotes = self.db.quotes.find_one({ 'id': ctx.guild.id })

        if quotes is not None or 'quotes' not in quotes:
            return await ctx.send('This server has no quotes')

        embed = PagedEmbed(f'All quotes for {ctx.guild.name}', f'{len(quotes["quotes"])} total')

        for idx, each in enumerate(quotes['quotes']):
            embed.add_field(name = f'Quote {idx}', value = each, inline = False)

        await ctx.send_pages(embed)

    @_quote.command(name = 'purge')
    @commands.has_permissions(administrator = True)
    async def _quote_purge(self, ctx):
        self.db.quotes.remove(
            { 'id': ctx.guild.id }
        )
        await ctx.send('Removed all quotes')

def setup(bot):
    bot.add_cog(Quotes(bot))