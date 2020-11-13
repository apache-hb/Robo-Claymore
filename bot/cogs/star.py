from discord import TextChannel, Embed
from discord.ext.commands import guild_only, group
from claymore.utils import wheel

def star_embed(author, msg):
    return Embed(
        title = '{0.name}#{0.discriminator}'.format(author),
        url = msg.jump_url,
        colour = author.colour,
        description = msg.content[:250] + (msg.content[250:] and '...')
    )

class Star(wheel(desc = 'starboard')):
    def __init__(self, bot):
        super().__init__(bot)

        @bot.listen()
        async def on_raw_reaction_add(event):
            guild = self.bot.get_guild(event.guild_id)
            chan = guild.get_channel(event.channel_id)
            user = event.member
            msg = await chan.fetch_message(event.message_id)

            if emote := await self.db.star.find_one({ 'id': user.guild.id }):
                if not (channel := user.guild.get_channel(emote['channel'])):
                    return

                num = len([react for react in msg.reactions if react.emoji == emote['emote']])
                if num >= emote.get('limit', 10):
                    await channel.send(embed = star_embed(msg.author, msg))

    @group(
        invoke_without_command = True,
        brief = 'set or disable the starboard',
        help = """
        &starboard #channel

        // the starboard has been enabled
        // and the bot will post starred messages
        // in #channel

        &starboard
        // the starboard is now disabled
        """
    )
    @guild_only()
    async def starboard(self, ctx, channel: TextChannel = None):
        if channel:
            await self.db.star.update_one(
                { 'id': ctx.guild.id },
                { '$set': { 'id': ctx.guild.id, 'channel': channel.id, 'limit': 10, 'emote': '⭐' } },
                upsert = True
            )
            await ctx.send(f'set starboard channel to {channel.name}')
        else:
            await self.db.star.update_one(
                { 'id': ctx.guild.id },
                { '$set': { 'id': ctx.guild.id, 'channel': 0 } },
                upsert = True
            )
            await ctx.send('disabled the starboard')

    @starboard.command(
        name = 'emote',
        brief = 'set starboard emote',
        help = """
        &starboard-emote 🦆

        // the starboard emote will now be 🦆
        // react to messages with 🦆 for them
        // to be send to the starboard
        """
    )
    async def starboard_emote(self, ctx, emote: str):
        await self.db.star.update_one(
            { 'id': ctx.guild.id },
            { '$set': { 'emote': emote } },
            upsert = True
        )
        await ctx.send(f'set the starboard emote to {emote}')

    @starboard.command(
        name = 'limit',
        brief = 'set the minimum amount of stars',
        help = """
        &starboard-limit 5
        
        // now any message that gets 5 or more star reacts 
        // will be put in the starboard
        """
    )
    async def starboard_limit(self, ctx, limit: int = 10):
        if limit < 1:
            return await ctx.send('limit must be greater than 0')

        await self.db.star.update_one(
            { 'id': ctx.guild.id },
            { '$set': { 'limit': limit } },
            upsert = True
        )
        await ctx.send(f'set new starboard limit to {limit}')

def setup(bot):
    bot.add_cog(Star(bot))
