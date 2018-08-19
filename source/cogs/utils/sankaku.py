#Requesting images from sankakucomplex

#credit to
#https://github.com/P0mf/scget/blob/master/scget
#for giving me some base code to reference for api calls

import aiohttp
import bs4

headers = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'
}

page = 'http://chan.sankakucomplex.com'

async def _request(url: str, headers: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = headers) as resp:
            if resp.status == 200:
                return await resp.text()

async def _request_subpage(sublink: str):
    resp = await _request(page + sublink, headers)
    try:
        soup = bs4.BeautifulSoup(resp, 'html.parser')
    except TypeError:
        return None
    for a in soup.findAll('a'):
        if a.get('href') is None:
            continue
        if a.get('href').startswith('//cs.sankakucomplex.com/data/sample'):
            continue
        elif a.get('href').startswith('//cs.sankakucomplex.com/data/'):
            return a.get('href') #get just one per subpage

async def skkcomplex_request(tags: str):
    soup = bs4.BeautifulSoup(await _request('https://chan.sankakucomplex.com/?tags={}&commit=Search'.format(tags), headers), 'html.parser')
    ret = []
    for a in soup.findAll('a'):
        if a.get('href').startswith('/post/show/'):
            b = await _request_subpage(str(a.get('href')))
            ret.append(b)
    return ret
