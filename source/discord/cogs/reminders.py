from claymore import Wheel
from discord.ext import commands, tasks
import discord
from datetime import datetime
import dateparser

class Reminders(Wheel):
    def __init__(self, bot):
        super().__init__(bot)
        self._reminder.start()

    def cog_unload(self):
        self._reminder.stop()

    @tasks.loop(seconds = 1.0)
    async def _reminder(self):
        now = datetime.now()
        rems = self.db.remind.find({ 'time': { '$lte': now }})
        for each in rems:
            try:
                await self.bot.get_user(each['author']).send(f'You asked to be remineded {each["msg"]}')
            except:
                pass
        self.db.remind.remove({ 'time': { '$lte': now }})

    @commands.command(name = 'remind')
    async def _remind(self, ctx, msg: str, *, time: str):
        time = dateparser.parse(time)
        if time <= datetime.now():
            return await ctx.send('Cannot remind you in the past')

        self.db.remind.insert_one({
            'author': ctx.message.author.id,
            'time': time,
            'msg': msg
        })

        await ctx.send('Added a reminder')

def setup(bot):
    bot.add_cog(Reminders(bot))