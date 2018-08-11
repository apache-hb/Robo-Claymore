from .store import try_file
import os
import time
import json

class SkyNet:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        print('Cog {} loaded'.format(self.__class__.__name__))

    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        if ctx.content.startswith(('!', '&', '/', '*', '$', '#')):
            return

        new = ''
        if ctx.guild is None:
            new = 'cogs/store/skynet/messages/'
        else:
            new = 'cogs/store/skynet/{0.guild.id}/'.format(ctx)

        os.makedirs(new, exist_ok = True)

        ret = json.load(try_file(new + '{}.json'.format(ctx.channel.id)))
        ret.append({
            'content': ctx.content,
            'meta': {
                'user': ctx.author.id,
                'name': ctx.author.name,
                'time': time.time()
            }
        })
        json.dump(ret, open(new + '{}.json'.format(ctx.channel.id), 'w'), indent = 4)


def setup(bot):
    bot.add_cog(SkyNet(bot))
