from discord.ext import commands
import discord
import random
import json

from .store import ball_awnsers, random_rigging, emoji, try_file

despacito = [
    '''Ay
Fonsi
DY
Oh
Oh no, oh no
Oh yeah
Diridiri, dirididi Daddy
Go
Sí, sabes que ya llevo un rato mirándote
Tengo que bailar contigo hoy (DY)
Vi que tu mirada ya estaba llamándome
Muéstrame el camino que yo voy (Oh)
Tú, tú eres el imán y yo soy el metal
Me voy acercando y voy armando el plan
Solo con pensarlo se acelera el pulso (Oh yeah)
Ya, ya me está gustando más de lo normal
Todos mis sentidos van pidiendo más
Esto hay que tomarlo sin ningún apuro
Despacito
Quiero respirar tu cuello despacito
Deja que te diga cosas al oído
Para que te acuerdes si no estás conmigo
Despacito''',
'''
Quiero desnudarte a besos despacito
Firmo en las paredes de tu laberinto
Y hacer de tu cuerpo todo un manuscrito (sube, sube, sube)
(Sube, sube)
Quiero ver bailar tu pelo
Quiero ser tu ritmo
Que le enseñes a mi boca
Tus lugares favoritos (favoritos, favoritos baby)
Déjame sobrepasar tus zonas de peligro
Hasta provocar tus gritos
Y que olvides tu apellido (Diridiri, dirididi Daddy)
Si te pido un beso ven dámelo
Yo sé que estás pensándolo
Llevo tiempo intentándolo
Mami, esto es dando y dándolo
Sabes que tu corazón conmigo te hace bom, bom
Sabes que esa beba está buscando de mi bom, bom
Ven prueba de mi boca para ver cómo te sabe
Quiero, quiero, quiero ver cuánto amor a ti te cabe
Yo no tengo prisa, yo me quiero dar el viaje
Empecemos lento, después salvaje
Pasito a pasito, suave suavecito
Nos vamos pegando poquito a poquito
Cuando tú me besas con esa destreza
Veo que eres malicia con delicadeza
Pasito a pasito, suave suavecito
Nos vamos pegando, poquito a poquito
Y es que esa belleza es un rompecabezas
Pero pa montarlo aquí tengo la pieza
Despacito''',
'''
Quiero respirar tu cuello despacito
Deja que te diga cosas al oído
Para que te acuerdes si no estás conmigo
Despacito
Quiero desnudarte a besos despacito
Firmo en las paredes de tu laberinto
Y hacer de tu cuerpo todo un manuscrito (sube, sube, sube)
(Sube, sube)
Quiero ver bailar tu pelo
Quiero ser tu ritmo
Que le enseñes a mi boca
Tus lugares favoritos (favoritos, favoritos baby)
Déjame sobrepasar tus zonas de peligro
Hasta provocar tus gritos
Y que olvides tu apellido
Despacito
Vamos a hacerlo en una playa en Puerto Rico
Hasta que las olas griten "¡ay, bendito!"
Para que mi sello se quede contigo
Pasito a pasito, suave suavecito
Nos vamos pegando, poquito a poquito
Que le enseñes a mi boca
Tus lugares favoritos (favoritos, favoritos baby)
Pasito a pasito, suave suavecito
Nos vamos pegando, poquito a poquito
Hasta provocar tus gritos
Y que olvides tu apellido (DY)
Despacito'''
]

class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.autoreact_list = json.load(try_file('cogs/store/autoreact.json'))
        self.hidden = False
        print('cog {} loaded'.format(self.__class__.__name__))

    @commands.command(name = "despacito")
    async def _despacito(self, ctx):
        for line in despacito:
            await ctx.send(line)

    @commands.command(name = "rate")
    async def _rate(self, ctx, *, thing: str):
        things = thing.lower().split(' ')
        ret = 0

        if not set(things).isdisjoint(random_rigging['bad']):
            ret = -1
        elif not set(things).isdisjoint(random_rigging['good']):
            ret = 11
        else:
            ret = random.randint(1, 10)

        await ctx.send('I rate ``{}`` a {} out of 10'.format(thing, ret))

    @commands.command(name = "coinflip")
    async def _coinflip(self, ctx, *, text: str = 'coinflip'):
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command(name = "8ball")
    async def _8ball(self, ctx, *, question: str):
        await ctx.send(random.choice(ball_awnsers))

    @commands.command(name = "compare",
    usage = 'compare <item1> and <item2>')
    async def _compare(self, ctx, *, items: str):
        ret = items.split('and')

        try:
            first = ret[0]
            second = ret[1]
        except IndexError:
            return await ctx.send('Please compare two diffrent things')

        if first.strip() in random_rigging['good']:
            awnser = 'is better than'
        elif second.strip() in random_rigging['good']:
            awnser = 'is worse than'
        elif first.strip() in random_rigging['bad']:
            awnser = 'is worse than'
        elif second.strip() in random_rigging['bad']:
            awsner = 'is better than'
        else:
            awnser = random.choice(['is better than', 'is worse than'])

        await ctx.send(first + awnser + second)

    def get_react_pair(self, phrase, react):
        return {
            'phrase': phrase,
            'react': react
        }

    async def on_message(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return

        for pair in self.autoreact_list:
            if pair['server_id'] == ctx.guild.id:
                for each in pair['reacts']:
                    if each['phrase'] in ctx.content.lower():
                        await ctx.add_reaction(each['react'][:-1])
                return
        self.autoreact_list.append({
            'server_id': ctx.guild.id,
            'reacts': []
        })
        json.dump(self.autoreact_list, open('cogs/store/autoreact.json', 'w'), indent = 4)

    @commands.group(invoke_without_command = True)
    async def autoreact(self, ctx):
        pass

    @autoreact.command(name = "add")
    async def _autoreact_add(self, ctx, *, text: str):
        pass

    @autoreact.command(name = "remove")
    async def _autoreact_remove(self, ctx, *, phrase: str):
        pass

    # @autoreact.command(name = "add")
    # async def _autoreact_add(self, ctx, *, text: str):
    #     text = text.split(' ')
    #     react = text[-1]
    #     phrase = ' '.join(text[:-1])

    #     if not emoji(react):
    #         return await ctx.send('you need to use an emoji as a reaction')

    #     for pair in autoreact:
    #         if pair['server_id'] == ctx.guild.id:
    #             for each in pair['reacts']:
    #                 if each['phrase'] == phrase.lower() and each['react'] == react:
    #                     return await ctx.send('you cannot add duplicates')

    #             pair['reacts'].append(self.get_react_pair(phrase.lower(), react))
    #             json.dump(autoreact, open('cogs/store/autoreact.json', 'w'), indent = 4)
    #             return await ctx.send('{} is now reacted with {}'.format(phrase, react))

    # @autoreact.command(name = "remove")
    # async def _autoreact_remove(self, ctx, *, phrase: str):
    #     for pair in autoreact:
    #         if pair['server_id'] == ctx.guild.id:
    #             for each in pair['reacts'][:]:
    #                 if each['phrase'] == phrase.lower():
    #                     pair['reacts'].remove(each)
    #                     json.dump(autoreact, open('cogs/store/autoreact.json', 'w'), indent = 4)
    #                     await ctx.send('{} is no longer reacted too'.format(phrase))

def setup(bot):
    bot.add_cog(Fun(bot))
