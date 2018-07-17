from discord.ext import commands
import random
import json

from .store import try_file, emoji

ball_awnsers = [
    'Definetly',
    'No',
    'Almost certain',
    'More than likley',
    'Perhaps',
    'Yes',
    'Certainly',
    'Not a chance',
    'Outlook good',
    'Of course',
    'Not a doubt about it'
]

random_rigging = {
    'good': ['apache', 'jeff', 'clay', 'ion'],
    'bad': ['autotitan', 'kotlin', 'ginger']
}

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
        self.autoreact_list = json.load(try_file('cogs/store/autoreact.json', '{}'))
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
    async def _coinflip(self, ctx):
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command(name = "8ball")
    async def _8ball(self, ctx):
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
            awnser = 'is better than'
        else:
            awnser = random.choice(['is better than', 'is worse than'])

        await ctx.send(first + awnser + second)

    async def on_message(self, ctx):
        if ctx.author.id == self.bot.user.id:
            return

        for (server, reacts) in self.autoreact_list.items():
            if server == str(ctx.guild.id):
                for (react, phrases) in reacts.items():
                    for each in phrases:
                        if each in ctx.content.lower():
                            await ctx.add_reaction(react)
                            break
                return

    #TODO: store metadata
    @commands.group(invoke_without_command = True)
    async def autoreact(self, ctx):
        pass

    @autoreact.before_invoke
    async def autoreact_ensure(self, ctx):
        for (guild, reacts) in self.autoreact_list.items():
            if guild == str(ctx.guild.id):
                return
        self.autoreact_list[ctx.guild.id] = {}

    @autoreact.command(name = "add")
    async def autoreact_add(self, ctx, *, text: str):
        text = text.split(' ')
        react = text[-1]
        phrase = ' '.join(text[:-1])
        if not emoji(react):
            return await ctx.send('Only emojis may be used as reactions')
        for (server, reacts) in self.autoreact_list.items():
            if server == str(ctx.guild.id):
                try:
                    if phrase in reacts[react]:
                        return await ctx.send('That is already an autoreact')
                    reacts[react].append(phrase)
                except KeyError:
                    reacts[react] = [phrase]
                return await ctx.send('``{}`` was added as an autoreact to ``{}``'.format(react, phrase))

    @autoreact.command(name = "remove")
    async def autoreact_remove(self, ctx, *, phrase: str):
        for (server, reacts) in self.autoreact_list.items():
            if server == str(ctx.guild.id):
                worked = False
                for (react, phrases) in reacts.items():
                    try:
                        phrases.remove(phrase)
                        worked = True
                    except KeyError:
                        continue
                if worked:
                    ret = '{} was removed as an autoreact phrase'
                else:
                    ret = '{} was not an autoreact phrase'
                return await ctx.send(ret.format(phrase))

    @autoreact_add.after_invoke
    @autoreact_remove.after_invoke
    async def autoreact_after(self, ctx):
        json.dump(self.autoreact_list, open('cogs/store/autoreact.json', 'w'), indent = 4)

def setup(bot):
    bot.add_cog(Fun(bot))
