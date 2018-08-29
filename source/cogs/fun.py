import copy
import json
import random
from ntpath import basename
from glob import glob
from io import BytesIO

import aiohttp
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from randomdict import RandomDict as rdict

from .utils import make_meme, make_retro, overlay_van, replace_eyes
from .utils.facial_detection import image_to_bytes
from .utils.networking import get_bytes, get_image, json_request
from .utils.shortcuts import emoji, quick_embed, try_file
from .utils.expanding_brain import make_expanding_brain

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

        #gather all the fonts into big and small versions
        self.small_fonts = rdict()
        self.big_fonts = rdict() #do this because you cant change font size later (idk why)

        for font_path in glob('cogs/fonts/*.ttf'):
            name = basename(font_path)

            #Load both a big and small version of the font
            self.small_fonts[name[:-4]] = ImageFont.truetype(font_path, size = 15)
            self.big_fonts[name[:-4]] = ImageFont.truetype(font_path, size = 54)

        #gather all the images of frothy for the `frothy` command
        self.frothy_images = [BytesIO(open(image, 'rb').read())
                                for image in glob('cogs/images/frothy/*.png')]

        #gather all the images of eyes for the `eyes` command
        self.eyes = rdict()
        for eye_path in glob('cogs/images/eyes/*.png'):
            name = basename(eye_path)
            #do [:-4] to trim off the `.png` ending
            self.eyes[name[:-4]] = Image.open(eye_path).convert('RGBA')

        self.youtube_crime = Image.open('cogs/images/crime.png', mode = 'r').convert('RGBA')

        print(f'cog {self.__class__.__name__} loaded')

    @commands.command(
        name = "frothy",
        description = "Im not very confident in my skills in many of the games i play",
        brief = "Frothy slowman"
    )
    async def _frothy(self, ctx, index: int = None):
        if index is None:
            image = random.choice(self.frothy_images)
        else:
            image = self.frothy_images.get()
            try:
                image = self.frothy_images[index]
            except IndexError:
                image = random.choice(self.frothy_images)
        f = discord.File(image, filename = 'frothy.png')
        await ctx.send(file = f)

    @commands.command(
        name = "despacito",
        description = "dump the entire lyrics to despacito into chat",
        brief = "despacito"
    )
    async def _despacito(self, ctx):
        for line in despacito:
            await ctx.send(line)

    @commands.command(
        name = "rate",
        description = "rate something on a scale of 1 to 10",
        brief = "rate a thing"
    )
    async def _rate(self, ctx, *, thing: str):
        thing = thing.lower()
        ret = 0

        if any(x in thing for x in random_rigging['bad']):
            ret = -1
        elif any(x in thing for x in random_rigging['good']):
            ret = 11
        else:
            ret = random.randint(1, 10)

        await ctx.send(f'I rate ``{thing}`` a {ret} out of 10')

    @commands.command(
        name = "coinflip",
        description = "flip a coin that can be heads or tails",
        brief = "50/50"
    )
    async def _coinflip(self, ctx):
        await ctx.send(random.choice(['Heads', 'Tails']))

    @commands.command(
        name = "8ball",
        description = "ask the magic 8ball a question",
        brief = "probably"
    )
    async def _8ball(self, ctx):
        await ctx.send(random.choice(ball_awnsers))

    @commands.command(
        name = "compare",
        usage = 'compare <item1> and <item2>',
        description = "compare two items to see which is better",
        brief = "comapre two items"
    )
    async def _compare(self, ctx, *, items: str):
        ret = items.split('and')

        try:
            first = ret[0]
            second = ret[1]
        except IndexError:
            return await ctx.send('Please compare two diffrent things')

        #this is just to rig the outcomes for certain things
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

        if ctx.guild is None:
            return

        for (server, reacts) in self.autoreact_list.items():
            if server == str(ctx.guild.id):
                for (react, phrases) in reacts.items():
                    for each in phrases:
                        if each in ctx.content.lower():
                            if react.endswith('>'):
                                await ctx.add_reaction(react[:-1])
                            else:
                                await ctx.add_reaction(react)
                            break
                return

    @commands.command(
        name = "duck",
        description = "now this, this i like",
        brief = "its a duck, it is perfect"
    )
    async def _duck(self, ctx):
        r = await json_request('https://api.random-d.uk/random')
        embed = quick_embed(ctx, 'ducks are the best animals')
        embed.set_image(url = r['url'])
        await ctx.send(embed = embed)

    @commands.command(
        name = "normie",
        description = "get a shit meme",
        brief = "REEEEEEEE"
    )
    async def _normie(self, ctx):
        j = await json_request('https://api.imgflip.com/get_memes')
        url = random.choice(j['data']['memes'])['url']
        await ctx.send(url)

    minecraft_api = 'https://mcgen.herokuapp.com/a.php?i=1&h=Achievement-{}&t={}'

    @commands.command(
        name = "minecraft",
        aliases = ['mc'],
        description = "create a custom minecraft achivement",
        brief = "get wood"
    )
    async def _minecraft(self, ctx, *, text: str):
        async with aiohttp.ClientSession() as session:
            url = self.minecraft_api.format(ctx.author.name, text)
            async with session.get(url) as resp:
                img = discord.File(BytesIO(await resp.read()), filename = 'minecraft.png')
                await ctx.send(file = img)

    @commands.command(
        name = "tombstone",
        aliases = ['tomb', 'grave'],
        description = "engrave a tombstone for a user",
        brief = "rip"
    )
    async def _tombstone(self, ctx, user: discord.User, *, text: str):
        if len(text) > 22:
            first = text[:22]
            second = text[22:]
            url = f'http://www.tombstonebuilder.com/generate.php?top1=R.I.P&top3={user.name}&top4={first}&top5={second}'
        else:
            url = f'http://www.tombstonebuilder.com/generate.php?top1=R.I.P&top3={user.name}&top4={text}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                img = discord.File(BytesIO(await resp.read()), filename = 'tombstone.png')
                await ctx.send(file = img)

    @commands.command(
        name = "crime",
        aliases = ['arrest', 'youtubecrime'],
        description = "arrest someone for youtube crime",
        brief = "stop, you have violated the law"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _crime(self, ctx, *, text: str):
        #make sure not to edit the original version
        base = copy.deepcopy(self.youtube_crime)

        draw_context = ImageDraw.Draw(base)
        draw_context.text((340, 125), text, (0, 0, 0), font = self.small_fonts['comic_sans'])

        output = image_to_bytes(base)

        ret = discord.File(output.getvalue(), filename = 'crime.png')
        await ctx.send(file = ret)

    @commands.command(
        name = "brain",
        description = "make an expanding brain meme",
        brief = "whomst'd've'y'aint"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _brain(self, ctx, *, text: str):
        txt = text.split('|')

        async with ctx.channel.typing():
            try:
                img = await make_expanding_brain(txt, self.big_fonts.random_item()[1])
            except IndexError:
                return await ctx.send('you must use between 2 and 6 phrases in a brain meme')

            f = discord.File(img.getvalue(), filename = 'brain.png')
            await ctx.send(file = f)

    @commands.command(
        name = "retro",
        description = "* V A P O R W A V E *",
        brief = "A S T H E T I C"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _retro(self, ctx, *, text: str):
        try:
            ret = await make_retro(text, random.choice(['2', '5', '4']))
        except TimeoutError:
            return await ctx.send('Server timed out')

        if ret is None:
            return await ctx.send('Server failed to proccess image')
        img = discord.File(await get_bytes(ret), filename = 'retro.jpg')

        await ctx.send(file = img)

    @commands.command(
        name = "eyes",
        aliases = ['eye'],
        description = "replace the eyes of an image with different eyes",
        brief = "lens flare makes for good retinas"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _eyes(self, ctx, eye: str = None):
        try:
            image = await get_bytes(await get_image(ctx))
        except TypeError:
            return await ctx.send('no image found (be sure to upload it directly as links dont work)')

        if eye is None:
            to_overlay = self.eye_dict.random_value()
        else:
            try:
                to_overlay = self.eye_dict[eye.lower()]
            except KeyError:
                return await ctx.send(f'``{eye}`` is not a valid eye')

        try:
            face = await replace_eyes(image, to_overlay)
        except LookupError:
            return await ctx.send('No eyes were found')
        except TypeError:
            return await ctx.send('That image is too big to proccess')

        ret = discord.File(face.getvalue(), filename = 'eye.png')
        await ctx.send(file = ret)

    @commands.command(
        name = "van",
        aliases = ['creepy', 'creep', 'creepvan'],
        description = "put someone in a creepy van",
        brief = "want some candy?"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _van(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        async with ctx.channel.typing():
            avatar = await get_bytes(user.avatar_url)

            img = await overlay_van(avatar)

            f = discord.File(img.getvalue(), filename = 'van.png')
            await ctx.send(file = f)

    @commands.command(
        name = "memegen",
        description = "turn an image into a meme with a header and footer",
        brief = " use '|' to split the text"
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _memegen(self, ctx, *, text: str = None):
        img = await get_bytes(await get_image(ctx))

        lst = text.split(' ')
        try:#the first word may be a font
            font = self.big_fonts[lst[0]]
        except KeyError:#if it isnt a font, just use a random one
            font = self.big_fonts.random_value()

        if text is None:#check non first because
            header = 'top text'
            footer = 'bottom text'
        elif '|' in text:#this raises an exception if text is None
            txt = text.split('|')
            header = txt[0][:15]
            footer = txt[1][:15]
        else:
            header = text[:15]
            footer = text[15:30]

        async with ctx.channel.typing():
            ret = make_meme(img, font, header = header, footer = footer)
            f = discord.File(ret.getvalue(), filename = 'meme.png')
            await ctx.send(file = f)

    @commands.command(
        name = "cat",
        description = "get a picture of a cat",
        brief = "cats are nice"
    )
    async def _cat(self, ctx):
        img = await get_bytes('https://cataas.com/cat')
        ret = discord.File(img, filename = 'cat.png')
        await ctx.send(file = ret)

    @commands.group(invoke_without_command = True)
    @commands.guild_only()
    async def autoreact(self, ctx):
        for (server, reacts) in self.autoreact_list.items():
            if int(server) == ctx.guild.id:
                if len(reacts) > 25:
                    all_reacts = [reacts[i:i + 24] for i in range(0, len(reacts), 24)]

                    for idx, each in enumerate(all_reacts):
                        embed = quick_embed(ctx, title = f'embed page ``{idx}``')
                        for key, page in each.items():
                            embed.add_field(name = key, value = '\n'.join(page))

                        await ctx.author.send(embed = embed)

                    return await ctx.send('i have sent the autoreacts to your inbox')

                else:
                    embed = quick_embed(ctx, title = 'all autoreacts')
                    for key, val in reacts.items():
                        if not val:
                            continue
                        embed.add_field(name = key, value = '\n'.join(val))

                    await ctx.author.send(embed = embed)

                    return await ctx.send('i sent the autoreacts to your inbox')
                return await ctx.send('there are no autoreacts for this server')

    @autoreact.command(
        name = "add",
        description = 'Adds an autoreact to a servers autoreact list',
        brief = "add an autoreact"
    )
    @commands.guild_only()
    async def autoreact_add(self, ctx, *, text: str):
        text = text.split(' ')
        react = text[-1]
        phrase = ' '.join(text[:-1])

        if not emoji(react):
            return await ctx.send(f'``{react}`` is not a thing i can react with')

        for (server, reacts) in self.autoreact_list.items():
            if int(server) == ctx.guild.id:
                try:
                    if phrase in reacts[react]:
                        return await ctx.send('that react has already been added')
                    reacts[react].append(phrase)
                except KeyError:
                    reacts[react] = [phrase]
                return await ctx.send(f'{react} is now added to messages that contain ``{phrase}``')

    @autoreact.command(
        name = "remove",
        description = "remove an autoreact from the current server",
        brief = "remove an autoreact"
    )
    @commands.guild_only()
    async def autoreact_remove(self, ctx, react: str):
        for (server, reacts) in self.autoreact_list.items():
            if int(server) == ctx.guild.id:
                try:
                    del reacts[react]
                    return await ctx.send(f'everything reacting to ``{react}`` has been removed')
                except KeyError:
                    return await ctx.send(f'couldnt find anything that reacted to {react}')

    @autoreact.before_invoke
    async def autoreact_before(self, ctx):
        for server in self.autoreact_list:
            if int(server) == ctx.guild.id:
                return#make sure the server exists
        self.autoreact_list[str(ctx.guild.id)] = {}
        #and create it if it doesnt exist

    @autoreact_add.after_invoke
    @autoreact_remove.after_invoke
    async def autoreact_after(self, _):
        json.dump(self.autoreact_list, open('cogs/store/autoreact.json', 'w'), indent = 4)

def setup(bot):
    bot.add_cog(Fun(bot))
