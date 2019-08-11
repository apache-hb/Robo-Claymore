import requests
from bs4 import BeautifulSoup as Soup

class EmojiConverter:
    def __init__(self):
        self.data = Soup(requests.get('https://unicode.org/emoji/charts/full-emoji-list.html').text)

    async def get_image(self, emoji):
        for each in self.data.find_all('tr'):
            for part in each.find_all('td'):
                print(part.find_all('img'))
        print(str(emoji))