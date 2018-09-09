"""
Module for scraping sankakucomplex.chan easily
Can be used externally
"""
#credit to
#https://github.com/P0mf/scget/blob/master/scget
#for giving me some base code to reference for api calls

from typing import List
import aiohttp
import bs4

HEADERS = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0'
}

PAGE = 'http://chan.sankakucomplex.com'

async def __request(url: str, headers: dict) -> str:
    """Request the raw text from the website with a query"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.text()

async def __request_subpage(sublink: str) -> str:
    """trauls through a page and finds all subpages"""
    resp = await __request(f'{PAGE}{sublink}', HEADERS)
    try:
        soup = bs4.BeautifulSoup(resp, 'html.parser')
    except TypeError:
        return None
    for each in soup.findAll('a'):
        if each.get('href') is None:
            continue
        if each.get('href').startswith('//cs.sankakucomplex.com/data/sample'):
            continue
        elif each.get('href').startswith('//cs.sankakucomplex.com/data/'):
            return each.get('href') #get just one per subPAGE


#so sankakucomplex has an api, but if you use it they ip ban you
#so we just scrape their website instead
#nice
async def skkcomplex_request(tags: str) -> List[str]:
    """Request a page by tags and get a response as a list of urls to images"""
    req = await __request(f'https://chan.sankakucomplex.com/?tags={tags}&commit=Search', HEADERS)
    soup = bs4.BeautifulSoup(req, 'html.parser')
    ret = []
    for each in soup.findAll('a'):
        if each.get('href').startswith('/post/show/'):
            page = await __request_subpage(str(each.get('href')))
            ret.append(page)
    return ret
