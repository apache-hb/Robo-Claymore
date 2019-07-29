import discord
from discord.ext import commands
from random import choice
from claymore import Wheel

class Autorole(Wheel):
    def __init__(self, bot):
        super().__init__(bot)

        self.bot.execute(
            """
            CREATE TABLE IF NOT EXISTS autorole (
                id INT NOT NULL,
                roles TEXT NOT NULL,
                random BOOLEAN NOT NULL,
                PRIMARY KEY(id)
            )
            """
        )

        self.bot.add_listener(self.on_member_join, 'on_member_join')

    async def on_member_join(self, member):
        query = self.select('roles', 'random')._from('autorole').where('id').equals(member.guild.id).execute().fetchone()

        if query is None:
            return

        random = query[1]
        roles = [int(i) for i in query[0].split(',')]
        
        if len(roles) < 2:
            random = False

        if not roles:
            return
        
        if random:
            role = choice(roles)
            try:
                await member.edit(roles = member.roles + [member.guild.get_role(choice(roles))])
            except discord.Forbidden:
                pass
            except discord.DiscordException:
                roles.remove(role)
        else:
            for role in roles:
                try:
                    await member.edit(roles = [member.guild.get_role(role)])
                except discord.Forbidden:
                    # ignore forbidden errors
                    pass
                except discord.DiscordException:
                    # if this throws an exception then the role cant exist
                    roles.remove(role)

        self.insert().or_replace_into('autorole').values(id = member.guild.id, roles = ','.join(map(str, roles)), random = random).execute()
                

    async def cog_check(self, ctx):
        if ctx.author.permissions_in(ctx.channel).administrator or ctx.author.id == self.bot.owner:
            return True
        await ctx.send('You need to be an admin to use this command')
        return False

    @commands.group(
        name = 'autorole', 
        invoke_without_command = True
    )
    async def _autorole(self, ctx):

        query = self.select('roles', 'random')._from('autorole').where('id').equals(ctx.guild.id).execute().fetchone()

        embed = ctx.make_embed(title = 'All autoroles', description = f'Autorole randomizer is {"enabled" if query and query[1] else "disabled"}')

        if query is None:
            embed.add_field(name = 'No autoroles', value = 'No roles will be given to new members')

            return await ctx.send(embed = embed)

        roles = map(int, query[0].split(','))

        for role in roles:
            embed.add_field(name = ctx.guild.get_role(role), value = str(role))

        await ctx.send(embed = embed)

    @_autorole.command(name = 'random')
    async def _autorole_toggle(self, ctx, new: str):
        if new.lower() == 'enable':
            enable = True
        elif new.lower() == 'disable':
            enable = False
        else:
            return await ctx.send('Command must be either `enable` or `disable`')

        roles = (self.select('roles')._from('autorole').where('id').equals(ctx.guild.id).execute().fetchone() or (''))[0]

        if len(roles.split(',')) < 2:
            return await ctx.send(f'Cannot {"enable" if enable else "disable"} randomness without at least 2 roles to pick between')

        self.insert().or_replace_into('autorole').values(id = ctx.guild.id, roles = ','.join(roles), random = enable).execute()

        await ctx.send(f'{"enable" if enable else "disable"}d autorole randomization')

    @_autorole.command(name = 'add')
    async def _autorole_add(self, ctx, role: discord.Role):
        query = self.select('roles')._from('autorole').where('id').equals(ctx.guild.id).execute().fetchone()

        if query is None:
            roles = []
        else:
            roles = [int(i) for i in query[0].split(',')]

        if role.id in roles:
            return await ctx.send(f'{role.name} is already an autorole')

        roles.append(role.id)

        self.insert().or_replace_into('autorole').values(id = ctx.guild.id, roles = ','.join(map(str, roles)), random = False).execute()
    
        embed = ctx.make_embed(title = 'All autoroles', description = 'Autoroles are added when users join')
        for role in map(ctx.guild.get_role, roles):
            embed.add_field(name = role.name, value = role.id)

        await ctx.send(embed = embed)

    @_autorole.command(name = 'remove')
    async def _autorole_remove(self, ctx, role: discord.Role):
        query = self.select('roles', 'random')._from('autorole').where('id').equals(ctx.guild.id).execute().fetchone()

        if query is None or not query[0]:
            return await ctx.send('There are no autoroles currently')

        roles = [int(r) for r in query[0].split(',')]
        random = query[1]

        if role.id not in roles:
            return await ctx.send(f'{role.name} is not a current autorole')

        roles.remove(role.id)

        if len(roles) < 2:
            random = False

        self.insert().or_replace_into('autorole').values(id = ctx.guild.id, roles = ','.join(map(str, roles)), random = random).execute()
        
        await ctx.send(f'removed {role.name} from the autorole list')

    @_autorole.command(name = 'reset')
    async def _autorole_reset(self, ctx):
        self.delete()._from('autorole').where('id').equals(ctx.guild.id).execute()
        await ctx.send('Removed all autoroles')

def setup(bot):
    bot.add_cog(Autorole(bot))