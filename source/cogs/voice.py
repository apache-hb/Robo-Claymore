from discord.ext import commands
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

yt_format = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_format = {
    'before_options': '-nostdin',
    'options': '-vn'
}
#TODO: Everything
ytdl = youtube_dl.YoutubeDL

class Voice:
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        print('cog {} loaded'.format(self.__class__.__name__))

    @commands.command(name = "play")
    async def _play(self, ctx, *, url: str):
        pass

def setup(bot):
    bot.add_cog(Voice(bot))