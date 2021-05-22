from claymore import Wheel, PagedEmbed
import discord
from discord.ext import commands
from random import choice

class Tags(Wheel):
    def desc(self):
        return 'tag text with a name'
        
    @commands.group(
        name = 'tag',
        brief = 'get a tag from the current server',
        invoke_without_command = True
    )
    @commands.guild_only()
    async def _tag(self, ctx, name: str = None):
        tags = await self.db.tags.find_one({ 'id': ctx.guild.id })

        del tags['id']
        del tags['_id']

        if tags is None:
            return await ctx.send('This server has no tags')

        if name is None:
            _, tag = choice(list(tags.items()))
            return await ctx.send(tag[0])

        try:
            await ctx.send(tags[name][0])
        except KeyError:
            await ctx.send(f'No tag with name `{name}`')

    @_tag.command(
        name = 'add',
        brief = 'add a tag to the current server'
    )
    async def _tag_add(self, ctx, name: str, *, content: str):
        await self.db.tags.update(
            { 'id': ctx.guild.id },
            { '$addToSet': { name: content } },
            upsert = True
        )

        await ctx.send(f'Created tag `{name}` if it did not already exist')

    @_tag.command(
        name = 'remove',
        brief = 'remove a tag from the current server'
    )
    async def _tag_remove(self, ctx, name: str):
        await self.db.tags.update(
            { 'id': ctx.guild.id },
            { '$unset': { name: "" } }
        )

        await ctx.send(f'Removed `{name}` if it was a tag')

    @_tag.command(
        name = 'list',
        brief = 'list all server tags'
    )
    async def _tag_list(self, ctx):
        tags = await self.db.tags.find_one({ 'id':ctx.guild.id })

        if tags is None:
            return await ctx.send('This server has no tags')

        del tags['id']
        del tags['_id']

        embed = PagedEmbed(f'All tags for {ctx.guild.name}', f'{len(tags)} total tags')

        for key, val in tags.items():
            embed.add_field(key, val, inline = False)

        await ctx.send_pages(embed)

    @_tag.command(
        name = 'purge',
        brief = 'remove all tags from the current server',
        aliases = [ 'reset', 'wipe', 'clean']
    )
    @commands.has_permissions(administrator = True)
    async def _tag_purge(self, ctx):
        await self.db.tags.remove({ 'id': ctx.guild.id })

        await ctx.send('Removed all tags')

def setup(bot):
    bot.add_cog(Tags(bot))