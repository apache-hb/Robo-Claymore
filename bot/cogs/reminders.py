from claymore import Wheel
from discord.ext import commands, tasks
import discord
from datetime import datetime
import dateparser

class Reminders(Wheel):
    def desc(self):
        return 'set reminders for yourself'

    def __init__(self, bot):
        super().__init__(bot)
        self._reminder.start()

    def cog_unload(self):
        self._reminder.stop()

    @tasks.loop(seconds = 1.0)
    async def _reminder(self):
        now = datetime.now()
        async for each in self.db.remind.find({ 'time': { '$lte': now }}):
            try:
                await self.bot.get_user(each['author']).send(f'You asked to be reminded about `{each["msg"]}`')
            except:
                pass
        
        await self.db.remind.delete_many({ 'time': { '$lte': now }})

    @commands.command(
        name = 'remind', 
        brief = 'create a reminder for yourself sometime in the future',
        aliases = [ 'remindme' ]
    )
    async def _remind(self, ctx, msg: str, *, time_fmt: str):
        time = dateparser.parse(time_fmt)
        try:
            if time <= datetime.now():
                return await ctx.send('Cannot remind you in the past')
        except:
            return await ctx.send(f'`{time_fmt}` could not be parsed')

        await self.db.remind.insert_one({
            'author': ctx.message.author.id,
            'time': time,
            'msg': msg
        })

        await ctx.send('Added a reminder')

def setup(bot):
    bot.add_cog(Reminders(bot))