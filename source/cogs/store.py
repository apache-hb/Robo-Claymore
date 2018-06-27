import json
import discord
import aiohttp
from urllib.request import pathname2url
from mimetypes import MimeTypes
from emoji import UNICODE_EMOJI as uemoji

MIME = MimeTypes()

#this is for the quote and tag system
class ServerNotFound(Exception):
    def __init__(self, server_id: int):
        self.server_id = server_id
#you better not add anymore custom exceptions


def can_override(ctx, user = None):
    if user is None:
        user = ctx.author
    return ctx.bot.is_owner(user) or user.id in whitelist

def quick_embed(ctx, title: str, description: str = None, colour: int = 0x023cfc):
    try: colour = ctx.me.colour
    except AttributeError: pass
    return discord.Embed(title = title, description = description, colour = colour)

async def tinyurl(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://tinyurl.com/api-create.php?url=' + url, timeout=10) as resp:
            return await resp.text()

async def hastebin(content: str):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://hastebin.com/documents', data = content.encode('utf-8')) as post:
            post = await post.json()
            return 'https://hastebin.com/' + post['key']

async def hastebin_error(ctx, content: str):
    embed = quick_embed(ctx, title = 'Too much text for me to send at once', description = 'But do not fear')
    embed.add_field(name = 'I have put it on hastebin for you', value = await hastebin(content))
    return embed

async def exists(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return int(await resp.status()) < 400

def embedable(url: str):
    url = pathname2url(url)
    mime_type = MIME.guess_type(url)
    return mime_type[0] in ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']

def emoji(emoji: str):
    #if the string is surrounded with <> there is a chance its a discord emoji
    if emoji.startswith('<') and emoji.endswith('>') and emoji.count(':') == 2:
        emoji = emoji[3:] if emoji.startswith('<a:') else emoji[2:]
        while not emoji.startswith(':'):
            emoji = emoji[1:]
        emoji = emoji[1:-1]
        if len(emoji):
            return True
        return False
    elif emoji in uemoji:
        return True
    return False

def only_mentions_bot(bot, context):

    if context.content.strip() == '<@!{}>'.format(bot.user.id):
        return True

    if context.content.strip() == '<@{}>'.format(bot.user.id):
        return True

    return False

config = json.load(open('cogs/store/config.json'))

whitelist = json.load(open('cogs/store/whitelist.json'))

blacklist = json.load(open('cogs/store/blacklist.json'))

logs = json.load(open('cogs/store/logs.json'))

tags = json.load(open('cogs/store/tags.json'))

quotes = json.load(open('cogs/store/quotes.json'))

autorole = json.load(open('cogs/store/autorole.json'))

autoreact = json.load(open('cogs/store/autoreact.json'))

# stolen from appuselfbot
# https://github.com/appu1232/Discord-Selfbot
emoji_dict = {
    'a': ['🇦 ', '🅰', '🍙', '🔼', '4⃣'],
    'b': ['🇧 ', '🅱', '8⃣'],
    'c': ['🇨 ', '©', '🗜'],
    'd': ['🇩 ', '↩'],
    'e': ['🇪 ', '3⃣', '📧', '💶'],
    'f': ['🇫 ', '🎏'],
    'g': ['🇬 ', '🗜', '6⃣', '9⃣', '⛽'],
    'h': ['🇭 ', '♓'],
    'i': ['🇮 ', 'ℹ', '🚹', '1⃣'],
    'j': ['🇯 ', '🗾'],
    'k': ['🇰 ', '🎋'],
    'l': ['🇱 ', '1⃣', '🇮', '👢', '💷'],
    'm': ['🇲 ', 'Ⓜ', '📉'],
    'n': ['🇳 ', '♑', '🎵'],
    'o': ['🇴 ', '🅾', '0⃣', '⭕', '🔘', '⏺', '⚪', '⚫', '🔵', '🔴', '💫'],
    'p': ['🇵 ', '🅿'],
    'q': ['🇶 ', '♌'],
    'r': ['🇷 ', '®'],
    's': ['🇸 ', '💲', '5⃣', '⚡', '💰', '💵'],
    't': ['🇹 ', '✝', '➕', '🎚', '🌴', '7⃣'],
    'u': ['🇺 ', '⛎', '🐉'],
    'v': ['🇻 ', '♈', '☑'],
    'w': ['🇼 ', '〰', '📈'],
    'x': ['🇽 ', '❎', '✖', '❌', '⚒'],
    'y': ['🇾 ', '✌', '💴'],
    'z': ['🇿 ', '2⃣'],
    '0': ['0⃣ ', '🅾', '0⃣', '⭕', '🔘', '⏺', '⚪', '⚫', '🔵', '🔴', '💫'],
    '1': ['1⃣ ', '🇮'],
    '2': ['2⃣ ', '🇿'],
    '3': ['3⃣ '],
    '4': ['4⃣ '],
    '5': ['5⃣ ', '🇸', '💲', '⚡'],
    '6': ['6⃣ '],
    '7': ['7⃣ '],
    '8': ['8⃣ ', '🎱', '🇧', '🅱'],
    '9': ['9⃣ '],
    '?': ['❓ '],
    '!': ['❗ ', '❕', '⚠', '❣'],
    ' ': ['   '],
    '\n': ['\n']
}

inverted_dict = {
    'a': 'ɐ',
    'b': 'q',
    'c': 'ɔ',
    'd': 'p',
    'e': 'ǝ',
    'f': 'ɟ',
    'g': 'ƃ',
    'h': 'ɥ',
    'i': 'ᴉ',
    'j': 'ɾ',
    'k': 'ʞ',
    'l': 'l',
    'm': 'ɯ',
    'n': 'u',
    'o': 'o',
    'p': 'd',
    'q': 'b',
    'r': 'ɹ',
    's': 's',
    't': 'ʇ',
    'u': 'n',
    'v': 'ʌ',
    'w': 'ʍ',
    'x': 'x',
    'y': 'ʎ',
    'z': 'z',
    ' ': ' ',
    '\n': '\n'
}

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

titanfall_pilot_variables = {
    'pilots': [
        'Grapple',
        'Pulse Blade',
        'Stim',
        'A-Wall',
        'Phase Shift',
        'Holo Pilot',
        'Cloak'
    ],
    'grenades': [
        'Frag Grenade',
        'Arc Grenade',
        'Fire Star',
        'Gravity Star',
        'Electric Smoke',
        'Satchel Charge'
    ],
    'primary': [
        'R201',
        'R101',
        'Hemlock',
        'G2A5',
        'Flatline',
        'Alternator',
        'CAR',
        'R-97',
        'Volt',
        'L-STAR',
        'Spitfire',
        'Devotion',
        'Double Take',
        'Kraber',
        'DMR',
        'EVA-8',
        'Mastiff',
        'Cold War',
        'EPG',
        'Softball',
        'SMR'
    ],
    'secondary': [
        'RE .45',
        'Hammond P2016',
        'Wingman Elite',
        'Mozambique',
        'Wingman B3',
    ],
    'anti_titan': [
        'Charge Rifle',
        'MGL',
        'Thunderbolt',
        'Archer'
    ],
    'perk_slot_a': [
        'Power Cell',
        'Fast Regen',
        'Ordinance Expert',
        'Phase Embark'
    ],
    'perk_slot_b': [
        'Wall Hang',
        'Kill Report',
        'Hover',
        'Low Profile'
    ]
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