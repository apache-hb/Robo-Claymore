from claymore.utils import wheel

class Star(wheel(desc = 'starboard')):
    pass

def setup(bot):
    bot.add_cog(Star(bot))
