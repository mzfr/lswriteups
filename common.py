import random
import aiohttp
from bs4 import BeautifulSoup


USER_AGENT_LIST = [
    '''Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
     Chrome/60.0.3112.90 Safari/537.36''',
    '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
    Chrome/44.0.2403.157 Safari/537.36''',
    '''Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    Chrome/60.0.3112.113 Safari/537.36''',
    '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    Chrome/57.0.2987.133 Safari/537.36''',
    '''Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    Chrome/57.0.2987.133 Safari/537.36''',

    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
]

USER_AGENT = random.choice(USER_AGENT_LIST)

HEADERS = {'user-agent': USER_AGENT}


async def make_soup(url):
    """Sends requests to a given URL and return BeautifulSoup format"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            soup = await response.read()

    return BeautifulSoup(soup.decode('utf-8'), "lxml")


def colors(string, color):
    """Makes thing color full :)"""
    return "\033[1;%sm%s\033[0m" % (color, string)
