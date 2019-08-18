from emoji import UNICODE_EMOJI as uemoji

def emoji(em: str) -> bool:
    if em.startswith('<') and em.endswith('>') and em.count(':') == 2:
        em = em[3:] if em.startswith('<a:') else em[2:]
        while not em.startswith(':'):
            em = em[1:]
        em = em[1:-1]
        return bool(em)

    return em in uemoji