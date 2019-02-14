
import enum

#all possible ranks people can have with the bot
class Ranks(enum.IntFlag):
    #they've been blocked from using the bot
    muted = 1

    #they're a normal user
    normal = 2

    #they've been granted privillige from the owner
    privillige = 4

    #they're the owner of the bot
    owner = 8

class Cog:

    def visibility() -> int:
        return Ranks.normal
    
    def name() -> str:
        return __class__.__name__