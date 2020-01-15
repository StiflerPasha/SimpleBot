import requests
import re

from bs4 import BeautifulSoup
from config import KEYS_SITE, HEADERS


def keys_parse(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'lxml')

        div = soup.findAll('div', attrs={'class': 'wall_post_text'})[0].text
        keys = re.findall(r'\d{14}', div)

        time = soup.findAll('span', attrs={'class': 'rel_date'})[0].text
        return time, keys
    else:
        print('ERROR')


if __name__ == '__main__':
    keys_parse(KEYS_SITE, HEADERS)
