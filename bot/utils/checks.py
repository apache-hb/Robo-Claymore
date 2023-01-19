from emoji import get_emoji_unicode_dict

uemoji = get_emoji_unicode_dict('en')

def emoji(em: str) -> bool:
    # check for custom discord emotes
    if em.startswith('<') and em.endswith('>') and em.count(':') == 2:
        em = em[3:] if em.startswith('<a:') else em[2:]
        while not em.startswith(':'):
            em = em[1:]
        em = em[1:-1]
        return bool(em)

    # fallback to checking the unicode emote table
    # TODO: we may want to remove the hardcoded locale in the future
    return em in uemoji['en']

def can_embed(url: str) -> bool:
    return any([t in url for t in ['.jpeg', '.png', '.gif', '.jpg']])
