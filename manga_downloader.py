
import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()
page = http.urlopen('GET', 'https://manganelo.com/chapter/yakusoku_no_neverland/chapter_125')
soup = BeautifulSoup(page.data, 'html.parser')
tags = soup.find_all('img')

for img in tags:
    print(img.get('src'))