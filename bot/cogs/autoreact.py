from claymore import Wheel, PagedEmbed
import discord
from discord.ext import commands
from utils import emoji

class AutoReact(Wheel):
    def desc(self):
        return 'automatically add reactions containing certain words or scentences'

    def __init__(self, bot):
        super().__init__(bot)
        bot.add_listener(self.on_message, 'on_message')

    async def on_message(self, message):
        reacts = await self.db.autoreact.find_one({ 'id': message.guild.id })

        if reacts:
            # a bit ugly but it makes iterating work
            del reacts['id']
            del reacts['_id']
            for react, phrases in reacts.items():
                for phrase in phrases:
                    if phrase in message.content:
                        await message.add_reaction(react)

    @commands.group(
        name = 'autoreact',
        brief = 'manage autoreacts for the current server',
        invoke_without_command = True
    )
    @commands.has_permissions(add_reactions = True)
    @commands.guild_only()
    async def _autoreact(self, ctx):
        reacts = await self.db.autoreact.find_one({ 'id': ctx.guild.id })

        # remove the fields we dont need
        if reacts:
            del reacts['id']
            del reacts['_id']

        # if there are still fields we do have autoreacts
        if not reacts:
            return await ctx.send(embed = ctx.make_embed('Autoreact', 'This server has no autoreacts'))

        embed = PagedEmbed('Autoreact', f'All autoreacts for {ctx.guild.name}')

        fields = {}

        for react, phrases in reacts.items():
            for phrase in phrases:
                try:
                    fields[phrase].append(react)
                except KeyError:
                    fields[phrase] = [react]

        for phrase, react in fields.items():
            embed.add_field(phrase, ' '.join(react), inline = False)

        await ctx.send_pages(embed)

    @_autoreact.command(
        name = 'purge',
        brief = 'remove all autoreacts for the current server',
        aliases = [ 'reset', 'wipe', 'clean']
    )
    @commands.has_permissions(administrator = True)
    async def _autoreact_purge(self, ctx):
        await self.db.autoreact.remove({ 'id': ctx.guild.id })

        await ctx.send('Removed all autoreacts')

    @_autoreact.command(
        name = 'add',
        brief = 'add an autoreact to the current server',
        usage = '<text> <emote>'
    )
    async def _autoreact_add(self, ctx, *, text: str):
        text = text.split()
        react = text[-1]
        phrase = ' '.join(text[:-1])

        if not emoji(react):
            return await ctx.send(f'`{react}` is not a valid autoreact')

        await self.db.autoreact.update(
            { 'id': ctx.guild.id },
            { '$addToSet': { react: phrase } },
            upsert = True
        )

        await ctx.send(f'Updated autoreacts to react with {react} to messages that contain `{phrase}`')

    @_autoreact.command(
        name = 'remove',
        brief = 'remove an autoreact from the current server'
    )
    async def _autoreact_remove(self, ctx, react: str):
        if not emoji(react):
            return await ctx.send(f'`{react}` is not a valid autoreact')

        await self.db.autoreact.update(
            { 'id': ctx.guild.id },
            { '$unset': { react: "" } }
        )

        await ctx.send(f'Updated autoreacts and removed everything {react} reacts to')

def setup(bot):
    bot.add_cog(AutoReact(bot))